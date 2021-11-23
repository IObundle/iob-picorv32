include $(CPU_DIR)/config.mk

MODULES+=$(MODULE)

VSRC+=$(CPU_SRC_DIR)/picorv32.v $(CPU_SRC_DIR)/iob_picorv32.v

#use hard multiplier and divider instructions
DEFINE+=$(defmacro)USE_MUL_DIV=$(USE_MUL_DIV)

#use compressed instructions
DEFINE+=$(defmacro)USE_COMPRESSED=$(USE_COMPRESSED)
