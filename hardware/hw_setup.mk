#RISC-V HARD MULTIPLIER AND DIVIDER INSTRUCTIONS
USE_MUL_DIV ?=0

#RISC-V COMPRESSED INSTRUCTIONS
USE_COMPRESSED ?=0


#
# Sources
#

SRC+=$(BUILD_VSRC_DIR)/picorv32.v
$(BUILD_VSRC_DIR)/picorv32.v: $(PICORV32_DIR)/hardware/src/picorv32.v
	cp $< $@

SRC+=$(BUILD_VSRC_DIR)/iob_picorv32.v
$(BUILD_VSRC_DIR)/iob_picorv32.v: $(PICORV32_DIR)/hardware/src/iob_picorv32.v
	cp $< $@

#use hard multiplier and divider instructions
DEFINE+=$(defmacro)USE_MUL_DIV=$(USE_MUL_DIV)

#use compressed instructions
DEFINE+=$(defmacro)USE_COMPRESSED=$(USE_COMPRESSED)
