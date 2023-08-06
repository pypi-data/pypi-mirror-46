
import base64
import datetime
import logging
import re
import time

from colibris import settings

from testmyesp import attributes
from testmyesp import flashimages
from testmyesp import instructions
from testmyesp import schemas

from testmyesp.hw import espctl
from testmyesp.hw import serial


ATTRIBUTE_MATCH_REGEX = re.compile(r'^{{([\w+]+)}}$')
ATTRIBUTE_FIND_REGEX = re.compile(r'{{([\w+]+)}}')

SERIAL_WAIT = 0.1  # seconds

logger = logging.getLogger(__name__)


class MemoryLogsHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        self._records = []
        self._instruction = None

        super().__init__(*args, **kwargs)

    def emit(self, record):
        record.instruction = self._instruction
        self._records.append(record)

    def set_instruction(self, instruction):
        self._instruction = instruction

    def reset(self):
        self._records.clear()
        self._instruction = None

    def get_records(self):
        return list(self._records)


class TestCase:
    def __init__(self, job, number, name, instructions, serial_baud=None, serial=None,
                 ensure_flash_images=None, reset_before=False):

        self.job = job
        self.number = number
        self.name = name
        self.instructions = instructions
        self.serial_baud = serial_baud
        self.serial = serial

        self.ensure_flash_images = ensure_flash_images
        self.reset_before = reset_before

        self.logger = logging.getLogger('{}.{}'.format(job.logger.name, name))
        self.memory_logs_handler = MemoryLogsHandler()
        self.logger.addHandler(self.memory_logs_handler)

        self.passed = None
        self.executed_instructions = []
        self.instruction_log = []
        self.main_serial_log = None
        self.instruction_serial_log = None

    def set_up(self):
        self.logger.debug('setting up')

        if self.ensure_flash_images or self.number == 1:
            if self.ensure_flash_images:
                self.logger.debug('ensuring flash images: %s', ', '.join(self.ensure_flash_images))

            else:
                self.logger.debug('flashing all images')

            espctl.reset_off()
            espctl.power_off()
            espctl.power_on()
            espctl.reset_on()

            self.close_serial_port()

            espctl.set_boot_mode(espctl.BOOT_MODE_FLASH)
            espctl.reset()

            flashimages.write_flash_images(self.job, self.ensure_flash_images)

            espctl.set_boot_mode(espctl.BOOT_MODE_NORMAL)
            espctl.reset()

        elif self.reset_before:
            espctl.reset_off()
            espctl.power_off()
            espctl.power_on()
            espctl.reset_on()

        attributes.reset()
        attributes.set(attributes.JOB_ID, self.job.id)
        attributes.set(attributes.TEST_CASE_NAME, self.name)

    def run(self):
        self.logger.debug('test case started')

        self.reset_instruction_serial_log()
        self.passed = True

        for instruction_dict in self.instructions:
            attributes.discover()  # new attributes might have shown up after last instruction
            instruction_dict['params'] = self.replace_attributes(instruction_dict.get('params', {}))

            self.memory_logs_handler.reset()

            if self.serial is None or self.serial.baudrate != self.serial_baud:
                self.logger.debug('opening serial port at %d', self.serial_baud)
                self.serial = serial.SerialWithLog(settings.SERIAL['port'], self.serial_baud)

            try:
                instruction = instructions.execute_instruction(self, instruction_dict, self.serial)
                self.executed_instructions.append(instruction)

            except Exception:
                self.logger.debug('test case failed')
                self.passed = False
                break

            finally:
                self.instruction_log += self.memory_logs_handler.get_records()
                self.instruction_serial_log += self.serial.read_available()

        else:
            self.logger.debug('test case succeeded')

        if self.serial:
            # wait a bit for any remaining serial data to be sent by device
            time.sleep(SERIAL_WAIT)
            self.serial.read_available()

            self.main_serial_log = self.serial.read_log
            self.serial.reset_log()

    def tear_down(self):
        self.logger.debug('tearing down')

        # only tear down executed instructions
        for instruction in self.executed_instructions:
            instruction.tear_down_test_case()

    def close_serial_port(self):
        if self.serial:
            self.logger.debug('closing serial port')
            self.serial.close()
            self.serial = None

    def get_instruction_serial_log(self):
        self.instruction_serial_log += self.serial.read_available()

        return self.instruction_serial_log

    def reset_instruction_serial_log(self):
        if self.serial:
            self.serial.read_available()
        self.instruction_serial_log = b''

    def get_result(self):
        return TestCaseResult(self, self.passed, self.instruction_log, self.main_serial_log)

    def replace_attributes(self, data):
        if isinstance(data, list):
            return [self.replace_attributes(e) for e in data]

        elif isinstance(data, dict):
            return {k: self.replace_attributes(v) for k, v in data.items()}

        elif isinstance(data, str):
            m = ATTRIBUTE_MATCH_REGEX.match(data)
            if m:
                attr_name = m.group(1)
                return attributes.get(attr_name, '')

            return ATTRIBUTE_FIND_REGEX.sub(lambda m: str(attributes.get(m.group(1), '')), data)

        else:
            return data


class TestCaseResult:
    def __init__(self, test_case, passed, instruction_log=None, serial_log=None):
        self.test_case_name = test_case.name
        self.passed = passed
        self.instruction_log = [self.log_record_to_dict(r) for r in instruction_log or []]
        self.serial_log = serial_log or b''

    @staticmethod
    def log_record_to_dict(record):
        return {
            'moment': datetime.datetime.utcfromtimestamp(int(record.created)).strftime('%Y-%m-%d %H:%M:%S'),
            'instruction': record.instruction.NAME if record.instruction else None,
            'level': record.levelname.lower(),
            'msg': record.getMessage(),
        }

    def to_dict(self):
        return {
            'name': self.test_case_name,
            'passed': self.passed,
            'instruction_log': self.instruction_log,
            'serial_log': base64.b64encode(self.serial_log).decode()
        }


def run_test_cases(job):
    test_case_list = schemas.TestCaseSchema(many=True).loads(job.test_cases_json)
    results = []
    all_executed_instructions = []
    prev_test_case = None

    for i, test_case_dict in enumerate(test_case_list):
        test_case = run_test_case(job, i + 1, prev_test_case, test_case_dict)
        result = test_case.get_result()
        results.append(result)
        all_executed_instructions += test_case.executed_instructions

        if not (result.passed or job.continue_on_failure):
            break

        prev_test_case = test_case

    job.logger.debug('tearing down')
    for instruction in all_executed_instructions:
        instruction.tear_down_job()

    return results


def run_test_case(job, number, prev_test_case, test_case_dict):
    serial = prev_test_case.serial if prev_test_case else None
    test_case = TestCase(job, number, serial=serial, **test_case_dict)

    test_case.set_up()
    test_case.run()
    test_case.tear_down()

    return test_case
