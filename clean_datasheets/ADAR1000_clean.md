# 8 GHz to 16 GHz, 4-Channel, X Band and Ku Band Beamformer


## FEATURES

8 GHz to 16 GHz frequency range

Half-duplex for transmit and receive modes

Single-pin transmit and receive control

360° phase adjustment range

2.8° phase resolution

≥31 dB gain adjustment range

≤0.5 dB gain resolution

Bias and control for external transmit and receive modules

Memory for 121 prestored beam positions

Four -20 dBm to +10 dBm power detectors

Integrated temperature sensor

Integrated 8-bit ADC for power detectors and temperature sen-
sor

Programmable bias modes

4-wire SPI interface


## APPLICATIONS

Phased array radar

Satellite communications systems


## GENERAL DESCRIPTION

The ADAR1000 is a 4-channel, X and Ku frequency band, beam-
forming core chip for phased arrays. This device operates in half-
duplex between receive and transmit modes. In receive mode, input
signals pass through four receive channels and are combined and
output at the common RF_IO pin. In transmit mode, the RF_IO
input signal is split and passes through the four transmit channels.
In both modes, the ADAR1000 provides a ≥31 dB gain adjustment
range and a full 360° phase adjustment range in each radio fre-
quency (RF) channel, with 6-bit resolution (less than ≤0.5 dB and
2.8°, respectively).

A simple 4-wire serial port interface (SPI) controls all of the on-chip
registers. In addition, two address pins allow SPI control of up
to four devices on the same serial lines. Dedicated transmit and
receive load pins also provide synchronization of all ADAR1000
chips in the same array, and a single pin controls fast switching
between the transmit and receive modes.

The ADAR1000 is fabricated in a silicon-germanium, bipolar CMOS
(BiCMOS) process. The device is available in a compact, 88-termi-
nal, 7 mm × 7 mm, LGA package and is specified from -40℃ to
+85℃.


## FUNCTIONAL BLOCK DIAGRAM


## Rev. B

# APPLICATIONS INFORMATION


## LNA BIAS OUTPUT CONTROL

The LNA_BIAS output voltage is controlled by a DAC, which in turn
is controlled by a combination of inputs (see Table 17).

The output is set by the LNA_BIAS_ON data when the ADAR1000
is in receive mode or LNA_BIAS_OFF data when in transmit mode,
if BIAS_CTRL is set to 1. If BIAS_CTRL set to 0, the output is set
by LNA_BIAS_ON data. See Table 18 for all control combinations.


Table 17. LNA Bias Output Control by Inputs

| Input | Bit/Pin Name | Description |
| Register 0x30 Bit 4 Bit 6 | LNA_BIAS_OUT_EN BIAS_CTRL | The LNA_BIAS output is enabled if LNA_BIAS_OUT_EN = 1. If LNA_BIAS_OUT_EN = 0, the output is open (three-state). Determines if the bias DAC always use the EXT_LNA_BIAS ON data (BIAS_CTRL = 0) or if the bias DAC can be controlled with the other inputs (BIAS_CTRL = 1). |
| Register 0x31 Bit 2 Bit 6 | TR_SOURCE RX_EN | Determines whether switching between transmit and receive mode is controlled by the SPI register or the TR input. Global receive enable. Logic high enables all four receive paths (if individual Chx_RX_EN bits are also logic high). See Figure 93. |
| Register 0x2D or from Several loca- tions in memory; see the memory map on the ADAR1000 product page. | EXT_LNA_BIAS_ON | External LNA Bias on data that can be sourced from multiple locations. |
| Register 0x4A or from Several loca- tions in memory; see the memory map on the ADAR1000 product page. | EXT_LNA_BIAS_OFF | External LNA Bias off data that can be sourced from multiple locations. |
| Input Pin | TR | Determines transmit or receive mode of chip when TR_SOURCE = 1 |


Table 18. Control of LNA_BIAS Output

| LNA_BIAS_OUT_EN (Register 0x030, Bit 4) | BIAS_CTRL (Register 0x030, Bit 6) | TR_SOURCE (Register 0x031, Bit 2) | RX_EN (Register 0x031, Bit 5) | TR (Input to Chip) | LNA Bias Bits Used |
| 0 | X1 ☒ | X1 ☒ | X1 ☒ | X1 ☒ | Open circuit (floating) |
| 1 | 0 ☐ | 0 ☐ | 0 ☐ | X1 ☒ | EXT_LNA_BIAS_ON |
| 1 | 0 ☐ | 0 ☐ | 1 | X1 ☒ | EXT_LNA_BIAS_ON |
| 1 | 1 | 0 ☐ | 0 ☐ | X1 ☒ | EXT_LNA_BIAS_OFF |
| 1 | 1 | 0 ☐ | 1 | X1 ☒ | EXT_LNA_BIAS_ON |
| 1 | 0 ☐ | 1 | 0 ☐ | 0 ☐ | EXT_LNA_BIAS_ON |
| 1 | 0 ☐ | 1 | 0 ☐ | 1 | EXT_LNA_BIAS_ON |
| 1 | 1 | 1 | 0 ☐ | 0 ☐ | EXT_LNA_BIAS_ON |
| 1 | 1 | 1 | 0 ☐ | 1 | EXT_LNA_BIAS_OFF |


1
☒
X means don't care.


### APPLICATIONS INFORMATION


#### PA BIAS, LNA BIAS, AND SWITCH BIAS SETUP EXAMPLES

Upon setup, all three sets of bias pins can either be controlled with
either the TR pin or with the SPI. Note the state of all the bias pins
upon power-up.

The PA_BIASx pins assume the EXT_PAx_BIAS_ON values
upon power-up. That is, all PA_BIASx pins are driven to 0 V.

The LNA_BIAS pin is floating upon power-up.

TR_SW_POS and TR_SW_NEG are floating upon power-up.


##### PA Bias Setup for TR Pin Control Example

Pull TR pin low to put the ADAR1000 into receive mode after TR
pin control is established. See Table 19 for the bit settings.


Table 19. Bias Bit Settings for TR Pin Control

| Register/Bit | Bit Setting | Description |
| Register 0x30, Bit 6 | BIAS_CTRL = 1 | Enables control of bias pins. |
| Register 0x31, Bit 2 | TR_SOURCE =1 | The TR pin controls trans- mit or receive device mode. |
| Register 0x38, Bit 5 | BIAS_RAM_BYPASS = 1 | Source all bias data from registers. |


Set the desired bias on and bias off values for the external PAs in
the following registers:

Register 0x29: EXT_PA1_BIAS_ON

Register 0x2A: EXT_PA2_BIAS_ON

Register 0x2B: EXT_PA3_BIAS_ON

Register 0x2C: EXT_PA4_BIAS_ON

Register 0x46: EXT_PA1_BIAS_OFF

Register 0x47: EXT_PA2_BIAS_OFF

Register 0x48: EXT_PA3_BIAS_OFF

Register 0x49: EXT_PA4_BIAS_OFF

After pulling the TR pin low and making these SPI writes, the
PA_BIASx pins assume the EXT_PAx_BIAS_OFF values. Pulling
the TR pin high causes the PA_BIASx pins to assume the
EXT_PÅx_BIAS_ON values. This setup example assumes that the
PA_ON pin is pulled high.


## PA Bias Setup for SPI Control Example

Set the bits as shown in Table 20.


Table 20. Bias Bit Settings for SPI Control

| Register/Bit | Bit Setting | Description |
| Register 0x30, Bit 6 | BIAS_CTRL = 1 | Enables control of bias pins. |
| Register 0x31 |  |  |
| Bit 1 | TR_SPI = 0 | Puts the ADAR1000 into Rx mode. |
| Bit 2 | TR_SOURCE = 0 | SPI controls transmit or receive device mode. |
| Bit 5 | RX_EN = 1 | Enable receive paths. |
| Bit 6 | TX_EN = 0 | Disables transmit paths. |
| Register 0x38, Bit 5 | BIAS_RAM_BYPASS = 1 | Source all bias data from registers. |


Set the desired bias on and bias off values for the external PAs in
the following registers:

Register 0x29: EXT_PA1_BIAS_ON

Register 0x2A: EXT_PA2_BIAS_ON

Register 0x2B: EXT_PA3_BIAS_ON

Register 0x2C: EXT_PA4_BIAS_ON

Register 0x46: EXT_PA1_BIAS_OFF

Register 0x47: EXT_PA2_BIAS_OFF

Register 0x48: EXT_PA3_BIAS_OFF

Register 0x49: EXT_PA4_BIAS_OFF

After making these SPI writes, the PA_BIASx pins assume the
EXT_PAx_BIAS_OFF values. Setting TX_EN = 1 causes the
PA_BIASx pins to assume the EXT_PAx_BIAS_ON values. It is
important to note that the PA_BIASx pins follow the TX_EN bit, not
the TR_SPI bit, while in SPI control.

The state of the TR and PA_ON pins have no effect on the
PA_BIASx pins while in SPI control mode.


## LNA Bias Setup for TR Pin Control Example

Pull TR pin low to put the ADAR1000 into receive mode after TR
pin control is established. Set the bits as shown in Table 21.


Table 21. LNA Bias Bit Settings for TR Pin Control

| Register/Bit | Bit Setting | Description |
| Register 0x30 Bit 4 Bit 6 | LNA_BIAS_OUT_EN = 1 BIAS_CTRL = 1 | Enables LNA bias driver. Enables control of bias pins. |
| Register 0x31 Bit 2 | TR_SOURCE = 1 | TR pin controls transmit or receive device mode. |
| Register 0x38, Bit 5 | BIAS_RAM_BYPASS = 1 | Source all bias data from registers. |


Set the desired bias on and bias off values for the external LNA in
the following registers:

Register 0x2D: EXT_LNA_BIAS_ON

Register 0x4A: EXT_LNA_BIAS_OFF
