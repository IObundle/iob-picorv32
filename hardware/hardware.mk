CPU_SRC_DIR:=$(CPU_DIR)/hardware/src
VSRC+=$(CPU_SRC_DIR)/picorv32.v $(CPU_SRC_DIR)/iob_picorv32.v

#use compressed instructions
ifeq ($(USE_COMPRESSED),1)
DEFINE+=$(defmacro)USE_COMPRESSED
endif
