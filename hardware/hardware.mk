ifeq ($(filter PICORV32, $(HW_MODULES)),)

include $(PICORV32_DIR)/config.mk

HW_MODULES+=PICORV32

#PATHS
PICORV32_SRC_DIR=$(PICORV32_DIR)/hardware/src

VSRC+=$(PICORV32_SRC_DIR)/picorv32.v $(PICORV32_SRC_DIR)/iob_picorv32.v

#use hard multiplier and divider instructions
DEFINE+=$(defmacro)USE_MUL_DIV=$(USE_MUL_DIV)

#use compressed instructions
DEFINE+=$(defmacro)USE_COMPRESSED=$(USE_COMPRESSED)

endif
