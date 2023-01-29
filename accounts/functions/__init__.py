from accounts.functions.jwt import (
    claim_token,
    expire,
    login,
    refresh,
    validate_token,
)
from accounts.functions.kavenegar import send_sms_otp
from accounts.functions.petshop_register import (
    apply_stage_0,
    apply_stage_1,
    apply_stage_2,
    apply_stage_3,
    check_petshop_register_stage,
)

apply_stage = [apply_stage_0, apply_stage_1, apply_stage_2, apply_stage_3]
