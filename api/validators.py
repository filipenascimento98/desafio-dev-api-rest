import re


class Validator:
    def validate_cpf(self, cpf):
        cpf = re.sub(r'\D', '', cpf)

        if len(cpf) != 11:
            return False

        sum_result = sum(int(cpf[i]) * (10 - i) for i in range(9))
        first_digit = (sum_result * 10 % 11) % 10

        sum_result = sum(int(cpf[i]) * (11 - i) for i in range(10))
        second_digit = (sum_result * 10 % 11) % 10

        return cpf[-2:] == f"{first_digit}{second_digit}"