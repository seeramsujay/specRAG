# 8-Bit, 500 MSPS, 1.8 V Analog-to-Digital Converter


## FEATURES

SNR = 47 dBFS at fin up to 250 MHz at 500 MSPS

ENOB of 7.5 bits at fin up to 250 MHz at 500 MSPS (-1.0 dBFS)
SFDR = 79 dBc at fin up to 250 MHz at 500 MSPS (-1.0 dBFS)
Integrated input buffer

Excellent linearity

DNL = ±0.1 LSB typical

INL = ±0.1 LSB typical

LVDS at 500 MSPS (ANSI-644 levels)

1 GHz full power analog bandwidth

On-chip reference, no external decoupling required

Low power dissipation
670 mW at 500 MSPS-LVDS SDR output

Programmable (nominal) input voltage range
1.18 V p-p to 1.6 V p-p, 1.5 V p-p nominal

1.8 V analog and digital supply operation

Selectable output data format (offset binary, twos
complement, Gray code)

Clock duty cycle stabilizer

Integrated data capture clock


## APPLICATIONS

Wireless and wired broadband communications

Cable reverse path

Communications test equipment

Low cost digital oscilloscopes

Satellite subsystems

Power amplifier linearization


## GENERAL DESCRIPTION

The AD9484 is an 8-bit, monolithic, sampling analog-to-digital
converter (ADC) optimized for high performance, low power,
and ease of use. The part operates at up to a 500 MSPS conver-
sion rate and is optimized for outstanding dynamic performance
in wideband carrier and broadband systems. All necessary
functions, including a sample-and-hold and voltage reference,
are included on the chip to provide a complete signal conversion
solution. The VREF pin can be used to monitor the internal
reference or provide an external voltage reference (external
reference mode must be enabled through the SPI port).

The ADC requires a 1.8 V analog voltage supply and a differen-
tial clock for full performance operation. The digital outputs are
LVDS (ANSI-644) compatible and support twos complement,
offset binary format, or Gray code. A data clock output is available
for proper output data timing.


## FUNCTIONAL BLOCK DIAGRAM


Fabricated on an advanced BiCMOS process, the AD9484 is availa-
ble in a 56-lead LFCSP, and is specified over the industrial
temperature range (-40°C to +85℃). This product is protected
by a U.S. patent.


## PRODUCT HIGHLIGHTS

1\.
High Performance.

Maintains 47 dBFS SNR at 500 MSPS with a 250 MHz input.

Ease of Use.

2\.
LVDS output data and output clock signal allow interface
to current FPGA technology. The on-chip reference and
sample-and-hold provide flexibility in system design. Use
of a single 1.8 V supply simplifies system power supply design.

3\.
Serial Port Control.

Standard serial port interface supports various product
functions, such as data formatting, power-down, gain
adjust, and output test pattern generation.


## Rev. A


# SPECIFICATIONS


## DC SPECIFICATIONS

AVDD = 1.8 V, DRVDD = 1.8 V, TMIN =- 40℃, TMAX=+85℃, fin =- 1.0 dBFS, full scale = 1.5 V, unless otherwise noted.


Table 1.

| Parameter1 | Temp | Min | Typ | Max | Unit |
| RESOLUTION |  |  | 8 |  | Bits |
| ACCURACY |  |  |  |  |  |
| No Missing Codes | Full |  | Guaranteed |  |  |
| Offset Error | 25°℃ |  | 0 |  | mV |
|  | Full | -3.0 |  | +3.0 | mV |
| Gain Error | 25°C |  | 1.0 |  | % FS |
|  | Full | -5.0 |  | +7.0 | % FS |
| Differential Nonlinearity (DNL) | 25°C |  | ±0.13 |  | LSB |
|  | Full | -0.25 |  | +0.25 | LSB |
| Integral Nonlinearity (INL) | 25°C |  | ±0.1 |  | LSB |
|  | Full | -0.15 |  | +0.15 | LSB |
| INTERNAL REFERENCE |  |  |  |  |  |
| VREF | Full | 0.71 | 0.75 | 0.78 | V |
| TEMPERATURE DRIFT |  |  |  |  |  |
| Offset Error | Full |  | 18 |  | μV/°C |
| Gain Error | Full |  | 0.07 |  | %/°℃ |
| ANALOG INPUTS (VIN+, VIN-) |  |  |  |  |  |
| Differential Input Voltage Range2 | Full | 1.18 | 1.5 | 1.6 | V p-p |
| Input Common-Mode Voltage | Full |  | 1.7 |  | V |
| Input Resistance (Differential) | Full |  | 1 |  | ΚΩ |
| Input Capacitance (Differential) | Full |  | 1.3 |  | pF |
| POWER SUPPLY |  |  |  |  |  |
| AVDD | Full | 1.75 | 1.8 | 1.9 | V |
| DRVDD | Full | 1.75 | 1.8 | 1.9 | V |
| Supply Currents |  |  |  |  |  |
| LAVDD 3 | Full |  | 283 | 300 | mA |
| IDRVDD3/SDR Mode4 | Full |  | 89 | 100 | mA |
| Power Dissipation |  |  |  |  |  |
| SDR Mode4 | Full |  | 670 | 720 | mW |
| Standby Mode | Full |  | 40 | 50 | mW |
| Power-Down Mode | Full |  | 2.5 | 7 | mW |


1 See the AN-835 Application Note, Understanding High Speed ADC Testing and Evaluation, for a complete set of definitions and how these tests were completed.

2 The input range is programmable through the SPI, and the range specified reflects the nominal values of each setting. See the Memory Map section.

3 LAVDD and IDRVDD are measured with a -1 dBFS, 10.3 MHz sine input at a rated sample rate.

4 Single data rate mode; this is the default mode of the AD9484.


## AC SPECIFICATIONS

AVDD = 1.8 V, DRVDD = 1.8 V, TMIN =- 40℃, TMAX=+85℃, fiN =- 1.0 dBFS, full scale = 1.5 V, unless otherwise noted.


Table 2.

| Parameter 1, 2 | Temp | Min | Typ | Max | Unit |
| SNR |  |  |  |  |  |
| fiN = 30.3 MHz | 25°℃ |  | 47.0 |  | dBFS |
| fiN = 70.3 MHz | 25°C |  | 47.0 |  | dBFS |
| fiN = 100.3 MHz | 25°C |  | 47.0 |  | dBFS |
|  | Full | 46.5 |  |  | dBFS |
| fiN = 250.3 MHz | 25°℃ |  | 47.0 |  | dBFS |
| fiN = 450.3 MHz | 25°℃ |  | 46.9 |  | dBFS |
| SINAD |  |  |  |  |  |
| fiN = 30.3 MHz | 25°℃ |  | 47.0 |  | dBFS |
| fin = 70.3 MHz | 25°C |  | 47.0 |  | dBFS |
| fiN = 100.3 MHz | 25°C |  | 47.0 |  | dBFS |
|  | Full | 46.4 |  |  | dBFS |
| fin = 250.3 MHz | 25°C |  | 47.0 |  | dBFS |
| fiN = 450.3 MHz | 25°C |  | 46.9 |  | dBFS |
| EFFECTIVE NUMBER OF BITS (ENOB) |  |  |  |  |  |
| fiN = 30.3 MHz | 25°℃ |  | 7.5 |  | Bits |
| fiN = 70.3 MHz | 25°℃ |  | 7.5 |  | Bits |
| fin = 100.3 MHz | 25°℃ |  | 7.5 |  | Bits |
| fin = 250.3 MHz | 25°C |  | 7.5 |  | Bits |
| fiN = 450.3 MHz | 25°C |  | 7.5 |  | Bits |
| WORST HARMONIC (SECOND or THIRD) |  |  |  |  |  |
| fiN = 30.3 MHz | 25°C |  | -87 |  | dBc |
| fin = 70.3 MHz | 25°℃ |  | -86 |  | dBc |
| fin = 100.3 MHz | 25°℃ |  | -87 |  | dBc |
|  | Full |  |  | -75 | dBc |
| fin = 250.3 MHz | 25°℃ |  | 83 |  | dBc |
| fiN = 450.3 MHz | 25°℃ |  | 70 |  | dBc |
| SFDR |  |  |  |  |  |
| fiN = 30.3 MHz | 25°℃ |  | 82 |  | dBc |
| fiN = 70.3 MHZ | 25°C |  | 81 |  | dBc |
| fiN = 100.3 MHz | 25°C |  | 82 |  | dBc |
|  | Full | 75 |  |  | dBc |
| fin = 250.3 MHz | 25°C |  | 79 |  | dBc |
| fiN = 450.3 MHz | 25°C |  | 70 |  | dBc |
| WORST OTHER HARMONIC (SFDR EXCLUDING SECOND and THIRD) |  |  |  |  |  |
| fiN = 30.3 MHz | 25°℃ |  | -82 |  | dBc |
| fin = 70.3 MHz | 25°C |  | -81 |  | dBc |
| fin = 100.3 MHz | 25°C |  | -82 |  | dBc |
|  | Full |  |  | -75 | dBc |
| fiN = 250.3 MHz | 25°℃ |  | 79 |  | dBc |
| fiN = 450.3 MHz | 25°℃ |  | 77 |  | dBc |
| TWO-TONE IMD |  |  |  |  |  |
| fiN1 = 119.5 MHz, fin2 = 122.5 MHz | 25°℃ |  | -77 |  | dBc |
| ANALOG INPUT BANDWIDTH |  |  |  |  |  |
| Full Power | 25°℃ |  | 1 |  | GHZ |


1 All ac specifications tested by driving CLK+ and CLK- differentially.

2 See the AN-835 Application Note, Understanding High Speed ADC Testing and Evaluation, for a complete set of definitions and how these tests were completed.


# DIGITAL SPECIFICATIONS

AVDD = 1.8 V, DRVDD = 1.8 V, TMIN =- 40℃, TMAX =+85℃, fin =- 1.0 dBFS, full scale = 1.5 V, unless otherwise noted.


Table 3.

| Parameter1 | Temp | Min | Typ | Max | Unit |
| CLOCK INPUTS |  |  |  |  |  |
| Logic Compliance | Full | CMOS/LVDS/LVPECL | | |  |
| Internal Common-Mode Bias | Full |  | 0.9 |  | V |
| Differential Input Voltage |  |  |  |  |  |
| High Level Input (VIH) | Full | 0.2 |  | 1.8 | V p-p |
| Low Level Input (VIL) | Full | -1.8 |  | -0.2 | V p-p |
| High Level Input Current (IIH) | Full | -10 |  | +10 | μΑ |
| Low Level Input Current (IIL) | Full | -10 |  | +10 | μΑ |
| Input Resistance (Differential) | Full | 8 | 10 | 12 | ΚΩ |
| Input Capacitance | Full |  | 4 |  | pF |
| LOGIC INPUTS |  |  |  |  |  |
| Logic 1 Voltage | Full | 0.8 x DRVDD |  |  | V |
| Logic 0 Voltage | Full |  |  | 0.2 × DRVDD | V |
| Logic 1 Input Current (SDIO, CSB) | Full |  | 0 |  | μΑ |
| Logic 0 Input Current (SDIO, CSB) | Full |  | -60 |  | μΑ |
| Logic 1 Input Current (SCLK, PDWN) | Full |  | 50 |  | μΑ |
| Logic 0 Input Current (SCLK, PDWN) | Full |  | 0 |  | μΑ |
| Input Capacitance | Full |  | 4 |  | pF |
| LOGIC OUTPUTS2 |  |  |  |  |  |
| VOD Differential Output Voltage | Full | 247 |  | 454 | mV |
| Vos Output Offset Voltage | Full | 1.125 |  | 1.375 | V |
| Output Coding |  |  |  |  |  |


1 See the AN-835 Application Note, Understanding High Speed ADC Testing and Evaluation, for a complete set of definitions and how these tests were completed.
2 LVDS RTERMINATION = 100 £2.


## SWITCHING SPECIFICATIONS

AVDD = 1.8 V, DRVDD = 1.8 V, TMIN =- 40℃, TMAX=+85℃, frN =- 1.0 dBFS, full scale = 1.5 V, unless otherwise noted.


Table 4.

| Parameter | Temp | Min | Typ | Max | Unit |
| Maximum Conversion Rate | Full | 500 |  |  | MSPS |
| Minimum Conversion Rate | Full |  |  | 50 | MSPS |
| CLK+ Pulse Width High (tCH)1 | Full | 0.9 |  | 11 | ns |
| CLK+ Pulse Width Low (tcL)1 | Full | 0.9 |  | 11 | ns |
| Output (LVDS-SDR)1 |  |  |  |  |  |
| Data Propagation Delay (tPD) | Full |  | 0.85 |  | ns |
| Rise Time (tR) (20% to 80%) | 25°℃ |  | 0.15 |  | ns |
| Fall Time (tr) (20% to 80%) | 25°℃ |  | 0.15 |  | ns |
| DCO Propagation Delay (tCPD) | Full |  | 0.6 |  | ns |
| Data to DCO Skew (tSKEw) | Full | -0.07 |  | +0.07 | ns |
| Latency | Full |  | 15 |  | Clock cycles |
| Aperture Time (tA) | 25°℃ |  | 0.85 |  | ns |
| Aperture Uncertainty (Jitter, t)) | 25°℃ |  | 80 |  | fs rms |


1 See Figure 2.


# ABSOLUTE MAXIMUM RATINGS


Table 5.

| Parameter | Rating |
| Electrical |  |
| AVDD to AGND | -0.3 V to +2.0 V |
| DRVDD to DRGND | -0.3 V to +2.0 V |
| AGND to DRGND | -0.3 V to +0.3 V |
| AVDD to DRVDD | -2.0 V to +2.0 V |
| D0+/D0- through D7+/D7- | -0.3 V to DRVDD + 0.2 V |
| to DRGND |  |
| DCO+, DCO- to DRGND | -0.3 V to DRVDD + 0.2 V |
| OR+, OR- to DRGND | -0.3 V to DRVDD + 0.2 V |
| CLK+ to AGND | -0.3 V to AVDD + 0.2 V |
| CLK- to AGND | -0.3 V to AVDD + 0.2 V |
| VIN+ to AGND | -0.3 V to AVDD + 0.2 V |
| VIN- to AGND | -0.3 V to AVDD + 0.2 V |
| SDIO/DCS to DRGND | -0.3 V to DRVDD + 0.2 V |
| PDWN to AGND | -0.3 V to DRVDD + 0.2 V |
| CSB to AGND | -0.3 V to DRVDD + 0.2 V |
| SCLK/DFS to AGND | -0.3 V to DRVDD + 0.2 V |
| CML to AGND | -0.3 V to AVDD + 0.2 V |
| VREF to AGND | -0.3 V to AVDD + 0.2 V |
| Environmental |  |
| Storage Temperature Range | -65°C to +125°℃ |
| Operating Temperature Range | -40°C to +85℃ |
| Lead Temperature | 300℃ |
| (Soldering, 10 sec) |
| Junction Temperature | 150℃ |


Stresses above those listed under Absolute Maximum Ratings
may cause permanent damage to the device. This is a stress
rating only; functional operation of the device at these or any
other conditions above those indicated in the operational
section of this specification is not implied. Exposure to absolute
maximum rating conditions for extended periods may affect
device reliability.


## THERMAL RESISTANCE

The exposed paddle must be soldered to the ground plane for
the LFCSP package. Soldering the exposed paddle to the PCB
increases the reliability of the solder joints, maximizing the
thermal capability of the package.


Table 6.

| Package Type | ΘJA | ΘJC | Unit |
| 56-Lead LFCSP_VQ (CP-56-5) | 23.7 | 1.7 | ºC/W |


Typical OJA and Ojc are specified for a 4-layer board in still air.
Airflow increases heat dissipation, effectively reducing OJA. In
addition, metal in direct contact with the package leads from
metal traces, through holes, ground, and power planes reduces
the OJA.


## ESD CAUTION


ESD (electrostatic discharge) sensitive device.
Charged devices and circuit boards can discharge
without detection. Although this product features
patented or proprietary protection circuitry, damage
may occur on devices subjected to high energy ESD.
Therefore, proper ESD precautions should be taken to
avoid performance degradation or loss of functionality.


### PIN CONFIGURATION AND FUNCTION DESCRIPTIONS

56 DNC

55 DNC

DNC

53

52 DNC

51 DNC

50 DCO+

49 DCO-

48 DRGND

47 DRVDD

AVDD

45 CLK-

44 CLK+

AVDD

43


NOTES

1\. DNC = DO NOT CONNECT. DO NOT CONNECT TO THIS PIN.

2\. AGND AND DRGND SHOULD BE TIED TO A COMMON
QUIET GROUND PLANE.

3\. THE EXPOSED PADDLE MUST BE SOLDERED TO
A GROUND PLANE.

09615-003


Table 7. Pin Function Descriptions

| Pin No. | Mnemonic | Description |
| 0 | AGND1 | Analog Ground. The exposed paddle must be soldered to a ground plane. |
| 30, 32 to 34, 37 to 39, 41 to 43, 46 | AVDD | 1.8 V Analog Supply. |
| 7,24, 47 | DRVDD | 1.8 V Digital Output Supply. |
| 8, 23, 48 | DRGND1 | Digital Output Ground. |
| 35 | VIN+ | Analog Input-True. |
| 36 | VIN- | Analog Input-Complement. |
| 40 | CML | Common-Mode Output. Enabled through the SPI, this pin provides a reference for the optimized internal bias voltage for VIN+/VIN -. |
| 44 | CLK+ | Clock Input-True. |
| 45 | CLK- | Clock Input-Complement. |
| 31 | VREF | Voltage Reference Internal/Input/Output. Nominally 0.75 V. |
| 1, 2, 28, 51 to 56 | DNC | Do Not Connect. Do not connect to this pin. This pin should be left floating. |
| 25 | SDIO | Serial Port Interface (SPI) Data Input/Output. |
| 26 | SCLK/DFS | Serial Port Interface Clock (Serial Port Mode)/Data Format Select (External Pin Mode). |
| 27 | CSB | Serial Port Chip Select (Active Low). |
| 29 | PWDN | Chip Power-Down. |
| 49 | DCO- | Data Clock Output-Complement. |
| 50 | DCO+ | Data Clock Output-True. |
| 3 | DO- | D0 Complement Output (LSB). |
| 4 | D0+ | D0 True Output (LSB). |
| 5 | D1- | D1 Complement Output. |
| 6 | D1+ | D1 True Output. |
| 9 | D2- | D2 Complement Output. |
| 10 | D2+ | D2 True Output. |
| 11 | D3- | D3 Complement Output. |
| 12 | D3+ | D3 True Output. |
| 13 | D4- | D4 Complement Output. |


46


| Pin No. | Mnemonic | Description |
| --- | --- | --- |
| 14 | D4+ | D4 True Output. |
| 15 | D5- | D5 Complement Output. |
| 16 | D5+ | D5 True Output. |
| 17 | D6- | D6 Complement Output. |
| 18 | D6+ | D6 True Output. |
| 19 | D7- | D7 Complement Output (MSB). |
| 20 | D7+ | D7 True Output (MSB). |
| 21 | OR- | Overrange Complement Output. |
| 22 | OR+ | Overrange True Output. |


1 Tie AGND and DRGND to a common quiet ground plane.


# TYPICAL PERFORMANCE CHARACTERISTICS

AVDD = 1.8 V, DRVDD = 1.8 V, rated sample rate, TA = 25℃, 1.5 V p-p differential input, AIN = - 1 dBFS, unless otherwise noted.


09615-106


09615-107


09615-108


09615-110


Figure 13. DNL, 500 MSPS


# EQUIVALENT CIRCUITS

AVDD

AVDD

AVDD

0.9V

15kQ2

15k22

CLK+ O

O CLK-

\+

09615-006


09615-025


Figure 27. Equivalent SDIO Input Circuit


# THEORY OF OPERATION

The AD9484 architecture consists of a front-end sample-and-
hold amplifier (SHA) followed by a pipelined switched capacitor
ADC. The quantized outputs from each stage are combined into
a final 8-bit result in the digital correction logic. The pipelined
architecture permits the first stage to operate on a new input
sample, whereas the remaining stages operate on preceding
samples. Sampling occurs on the rising edge of the clock.

Each stage of the pipeline, excluding the last, consists of a low
resolution flash ADC connected to a switched capacitor DAC
and interstage residue amplifier (MDAC). The residue amplifier
magnifies the difference between the reconstructed DAC output
and the flash input for the next stage in the pipeline. One bit of
redundancy is used in each stage to facilitate digital correction
of flash errors. The last stage simply consists of a flash ADC.

The input stage contains a differential SHA that can be ac- or
dc-coupled in differential or single-ended mode. The output
staging block aligns the data, carries out the error correction,
and passes the data to the output buffers. The output buffers
are powered from a separate supply, allowing adjustment of the
output voltage swing. During power-down, the output buffers
enter a high impedance state.


## ANALOG INPUT AND VOLTAGE REFERENCE

The analog input to the AD9484 is a differential buffer. For best
dynamic performance, match the source impedances driving
VIN+ and VIN- such that common-mode settling errors are
symmetrical. The analog input is optimized to provide superior
wideband performance and requires that the analog inputs be
driven differentially. SNR and SINAD performance degrades
significantly if the analog input is driven with a single-ended
signal.

A wideband transformer, such as Mini-Circuits® ADT1-1WT,
can provide the differential analog inputs for applications that
require a single-ended-to-differential conversion. Both analog
inputs are self-biased by an on-chip reference to a nominal 1.7 V.

An internal differential voltage reference creates positive and
negative reference voltages that define the 1.5 V p-p fixed span
of the ADC core. This internal voltage reference can be adjusted
by means of SPI control. See the AD9484 Configuration Using
the SPI section for more details.


## Differential Input Configurations

Optimum performance is achieved while driving the AD9484
in a differential input configuration. For baseband applications,
the AD8138 differential driver provides excellent performance
and a flexible interface to the ADC. The output common-mode
voltage of the AD8138 is easily set to AVDD/2 + 0.5 V, and the
driver can be configured in a Sallen-Key filter topology to pro-
vide band limiting of the input signal.


At input frequencies in the second Nyquist zone and above, the
performance of most amplifiers may not be adequate to achieve
the true performance of the AD9484. This is especially true in
IF undersampling applications where frequencies in the 70 MHz
to 100 MHz range are being sampled. For these applications,
differential transformer coupling is the recommended input
configuration. The signal characteristics must be considered
when selecting a transformer. Most RF transformers saturate at
frequencies below a few megahertz (MHz), and excessive signal
power can cause core saturation, which leads to distortion.

In any configuration, the value of the shunt capacitor, C (see
Figure 30), is dependent on the input frequency and may need
to be reduced or removed.


As an alternative to using a transformer-coupled input at frequen-
cies in the second Nyquist zone, the AD8352 differential driver
can be used (see Figure 30).


# CLOCK INPUT CONSIDERATIONS

For optimum performance, drive the AD9484 sample clock
inputs (CLK+ and CLK-) with a differential signal. This signal
is typically ac-coupled into the CLK+ and CLK- pins via a
transformer or capacitors. These pins are biased at ~0.9 V
internally and require no additional bias. If the clock signal is
dc-coupled, then the common-mode voltage should remain
within a range of 0.9 V.

Figure 33 shows one preferred method for clocking the AD9484.
The low jitter clock source is converted from single-ended to
differential using an RF transformer. The back-to-back Schottky
diodes across the secondary transformer limit clock excursions
into the AD9484 to approximately 0.8 V p-p differential. This
helps prevent the large voltage swings of the clock from feeding
through to other portions of the AD9484 and preserves the fast
rise and fall times of the signal, which are critical to low jitter
performance.


If a low jitter clock is available, another option is to ac couple a
differential PECL signal to the sample clock input pins, as
shown in Figure 31. The AD9510/AD9511/AD9512/AD9513/
AD9514/AD9515 family of clock drivers offers excellent jitter
performance.

In some applications, it may be acceptable to drive the sample
clock inputs with a single-ended 1.8 V CMOS signal. In such
applications, drive the CLK+ pin directly from a CMOS gate,
and bypass the CLK- pin to ground with a 0.1 µF capacitor in
parallel with a 39 kl2 resistor (see Figure 34).


Figure 34. Single-Ended 1.8 V CMOS Input Clock (Up to 200 MHz)


## Clock Duty Cycle Considerations

Typical high speed ADCs use both clock edges to generate a
variety of internal timing signals. As a result, these ADCs may
be sensitive to clock duty cycle. A 5% tolerance is commonly
required on the clock duty cycle to maintain dynamic performance
characteristics. The AD9484 contains a duty cycle stabilizer (DCS)
that retimes the nonsampling edge, providing an internal clock
signal with a nominal 50% duty cycle. This allows a wide range
of clock input duty cycles without affecting the performance of
the AD9484. When the DCS is on, noise and distortion perfor-
mance are nearly flat for a wide range of duty cycles.

The duty cycle stabilizer uses a delay-locked loop (DLL) to
create the nonsampling edge. As a result, any changes to the
sampling frequency require approximately 15 clock cycles
to allow the DLL to acquire and lock to the new rate.


## Clock Jitter Considerations

High speed, high resolution ADCs are sensitive to the quality of the
clock input. The degradation in SNR at a given input frequency
(f) due only to aperture jitter (tj) can be calculated by

SNR Degradation = 20 x log10(1/2 × Tt x fax t])

In this equation, the rms aperture jitter represents the root mean
square of all jitter sources, including the clock input, analog input
signal, and ADC aperture jitter specifications. IF undersampling
applications are particularly sensitive to jitter (see Figure 35).

Treat the clock input as an analog signal in cases where aperture
jitter may affect the dynamic range of the AD9484. Separate the
power supplies for clock drivers from the ADC output driver
supplies to avoid modulating the clock signal with digital noise.
Low jitter, crystal-controlled oscillators make the best clock
sources. If the clock is generated from another type of source
(by gating, dividing, or other methods), it should be retimed by
the original clock at the last step.

Refer to the AN-501 Application Note and the AN-756
Application Note for more in-depth information about jitter
performance as it relates to ADCs (visit www.analog.com).


# POWER DISSIPATION AND POWER-DOWN MODE

As shown in Figure 18, the power dissipated by the AD9484 is
proportional to its sample rate. The digital power dissipation
does not vary much because it is determined primarily by the
DRVDD supply and bias current of the LVDS output drivers.

By asserting PDWN (Pin 29) high, the AD9484 is placed in
standby mode or full power-down mode, as determined by the
contents of Serial Port Register 08. Reasserting the PDWN pin
low returns the AD9484 to its normal operational mode.

An additional standby mode is supported by means of varying
the clock input. When the clock rate falls below 50 MHz, the
AD9484 assumes a standby state. In this case, the biasing network
and internal reference remain on, but digital circuitry is powered
down. Upon reactivating the clock, the AD9484 resumes normal
operation after allowing for the pipeline latency.


# DIGITAL OUTPUTS Digital Outputs and Timing

The AD9484 differential outputs conform to the ANSI-644
LVDS standard on default power-up. This can be changed to a
low power, reduced signal option similar to the IEEE 1596.3
standard using the SPI. This LVDS standard can further reduce
the overall power dissipation of the device, which reduces the
power by ~39 mW. See the Memory Map section for more infor-
mation. The LVDS driver current is derived on chip and sets
the output current at each output equal to a nominal 3.5 mA.
A 100 Q2 differential termination resistor placed at the LVDS
receiver inputs results in a nominal 350 mV swing at the receiver.

The AD9484 LVDS outputs facilitate interfacing with LVDS
receivers in custom ASICs and FPGAs that have LVDS capability
for superior switching performance in noisy environments.
Single point-to-point net topologies are recommended with a
100 22 termination resistor placed as close to the receiver as
possible. No far-end receiver termination or poor differential
trace routing may result in timing errors. It is recommended
that the trace length be no longer than 24 inches and that the


differential output traces be kept close together and at equal
lengths.

An example of the LVDS output using the ANSI standard (default)
data eye and a time interval error (TIE) jitter histogram with
trace lengths less than 24 inches on regular FR-4 material is
shown in Figure 36. Figure 37 shows an example of when the
trace lengths exceed 24 inches on regular FR-4 material. Notice
that the TIE jitter histogram reflects the decrease of the data eye
opening as the edge deviates from the ideal position. It is up to
the user to determine if the waveforms meet the timing budget
of the design when the trace lengths exceed 24 inches.


The format of the output data is offset binary by default. An
example of the output coding format can be found in Table 11.
If it is desired to change the output data format to twos comple-
ment, see the AD9484 Configuration Using the SPI section.

An output clock signal is provided to assist in capturing data
from the AD9484. The DCO is used to clock the output data
and is equal to the sampling clock (CLK) rate. In single data
rate mode (SDR), data is clocked out of the AD9484 and must
be captured on the rising edge of the DCO. See the timing
diagram shown in Figure 2 for more information.


# Output Data Rate and Pinout Configuration

The output data of the AD9484 can be configured to drive
12 pairs of LVDS outputs at the same rate as the input clock
signal (SDR mode).


## Out-of-Range (OR)

An out-of-range condition exists when the analog input voltage
is beyond the input range of the ADC. OR+ and OR- (OR+)
are digital outputs that are updated along with the data output
corresponding to the particular sampled input voltage. Thus,
OR+ has the same pipeline latency as the digital data. OR+ is
low when the analog input voltage is within the analog input
range and high when the analog input voltage exceeds the input
range, as shown in Figure 38. OR+ remains high until the analog
input returns to within the input range and another conversion
is completed. By logically AND'ing OR+ with the MSB and its
complement, overrange high or underrange low conditions can
be detected.


# TIMING

The AD9484 provides latched data outputs with a pipeline delay
of 15 clock cycles. Data outputs are available one propagation
delay (tpD) after the rising edge of the clock signal.

Minimize the length of the output data lines and loads placed
on them to reduce transients within the AD9484. These transi-
ents can degrade the dynamic performance of the converter.
The AD9484 also provides a data clock output (DCO) intended
for capturing the data in an external register. The data outputs
are valid on the rising edge of DCO.

The lowest conversion rate of the AD9484 is 50 MSPS. At clock
rates below 1 MSPS, the AD9484 assumes the standby mode.


## VREF

The AD9484 VREF pin (Pin 31) allows the user to monitor the
on-board voltage reference, or provide an external reference
(requires configuration through the SPI). The three optional
settings are internal VREF (pin is connected to 20 k£2 to ground),
export VREF, and import VREF. Do not attach a bypass capacitor
to this pin. VREF is internally compensated and additional
loading may impact performance.


# AD9484 CONFIGURATION USING THE SPI

The AD9484 SPI allows the user to configure the converter for
specific functions or operations through a structured register
space inside the ADC. This gives the user added flexibility to
customize device operation depending on the application.
Addresses are accessed (programmed or readback) serially in
1-byte words. Each byte can be further divided into fields,
which are documented in the Memory Map section.

There are three pins that define the serial port interface (SPI) to
this particular ADC. They are the SCLK/DFS, SDIO and CSB
pins. The SCLK/DFS (serial clock) is used to synchronize the
read and write data presented the ADC. The SDIO (serial data
input/output) is a dual-purpose pin that allows data to be sent
to and read from the internal ADC memory map registers. The
CSB is an active low control that enables or disables the read
and write cycles (see Table 8).


Table 8. Serial Port Pins

| Mnemonic | Function |
| SCLK | SCLK (serial clock) is the serial shift clock in. SCLK is used to synchronize serial interface reads and writes. |
| SDIO CSB | SDIO (serial data input/output) is a dual-purpose pin. The typical role for this pin is an input and output depending on the instruction being sent and the relative position in the timing frame. CSB (chip select) is an active low control that gates the read and write cycles. |


The falling edge of the CSB, in conjunction with the rising edge
of the SCLK, determines the start of the framing. An example of
the serial timing and its definitions can be found in Figure 39
and Table 10.

During an instruction phase, a 16-bit instruction is transmitted.
Data then follows the instruction phase and is determined by
the W0 and W1 bits, which is one or more bytes of data. All
data is composed of 8-bit words. The first bit of each individual
byte of serial data indicates whether this is a read or write

command. This allows the serial data input/output (SDIO) pin
to change direction from an input to an output.

Data can be sent in MSB or in LSB first mode. MSB first is
default on power-up and can be changed by changing the
configuration register. For more information about this feature
and others, see the AN-877 Application Note, Interfacing to
High Speed ADCs via SPI at www.analog.com.


## HARDWARE INTERFACE

The pins described in Table 8 comprise the physical interface
between the programming device of the user and the serial port
of the AD9484. The SCLK pin and the CSB pin function as
inputs when using the SPI interface. The SDIO pin is bidirec-
tional, functioning as an input during the write phase and as an
output during readback.

This interface is flexible enough to be controlled by either
PROMs or PIC® microcontrollers as well. This provides the user
with an alternate method to program the ADC other than a SPI
controller.

If the user chooses not to use the SPI interface, some pins serve
a dual function and are associated with a specific function when
strapped externally to AVDD or ground during device power-
on. The Configuration Without the SPI section describes the
strappable functions supported on the AD9484.


## CONFIGURATION WITHOUT THE SPI

In applications that do not interface to the SPI control registers,
the SCLK/DFS pin can alternately serve as a standalone CMOS-
compatible control pin. Connect the CSB pin to AVDD, which
disables the serial port interface.


Table 9. Mode Selection

| Mnemonic | External Voltage | Configuration |
| SCLK/DFS | AVDD AGND | Twos complement enabled Offset binary enabled |


Table 10. Serial Timing Definitions

| Parameter | Minimum (ns) | Description |
| tos | 5 | Setup time between the data and the rising edge of SCLK |
| tDH | 2 | Hold time between the data and the rising edge of SCLK |
| tCLK | 40 | Period of the clock |
| ts | 5 | Setup time between CSB and SCLK |
| tH | 2 | Hold time between CSB and SCLK |
| tHIGH | 16 | Minimum period that SCLK should be in a logic high state |
| tLow | 16 | Minimum period that SCLK should be in a logic low state |
| tEN_SDIO | 1 | Minimum time for the SDIO pin to switch from an input to an output relative to the SCLK falling edge (not shown in Figure 39) |
| tDIS_SDIO | 5 | Minimum time for the SDIO pin to switch from an output to an input relative to the SCLK rising edge (not shown in Figure 39) |


Table 11. Output Data Format

| Input (V) | Condition (V) | Offset Binary Output Mode, D7± to D0± | Twos Complement Mode, D7+ to DO± | OR± |
| VIN+ - VIN- | <- 0.75 - 0.5 LSB | 0000 0000 | 1000 0000 | 1 |
| VIN+ - VIN- | =- 0.75 | 0000 0000 | 1000 0000 | 0 |
| VIN+ - VIN- | = 0 | 1000 0000 | 0000 0000 | 0 |
| VIN+ - VIN- | = 0.75 | 1111 1111 | 0111 1111 | 0 |
| VIN+ - VIN- | > 0.75 + 0.5 LSB | 1111 1111 | 0111 1111 | 1 |


# MEMORY MAP READING THE MEMORY MAP TABLE

Each row in the memory map table (see Table 12) has eight
address locations. The memory map is roughly divided into
three sections: chip configuration register map (Address 0x00 to
Address 0x02), transfer register map (Address 0xFF), and ADC
functions register map (Address 0x08 to Address 0x2A).

The Addr. (Hex) column of the memory map indicates the register
address in hexadecimal, and the Default Value (Hex) column
shows the default hexadecimal value that is already written into
the register. The Bit 7 (MSB) column is the start of the default
hexadecimal value given. For example, Hexadecimal Address
0x2A, OVR_CONFIG, has a hexadecimal default value of 0x01.
This means Bit 7 = 0, Bit 6 = 0, Bit 5 = 0, Bit 4 = 0, Bit 3 = 0,
Bit 2 = 0, Bit 1 = 0, and Bit 0 = 1, or 0000 0001 in binary. The
default value enables the OR+ output. Overwriting this default so
that Bit 0 = 0 disables the OR+ output. For more information on
this and other functions, consult the AN-877 Application Note,
Interfacing to High-Speed ADCs via SPI® user manual at
www.analog.com.


## RESERVED LOCATIONS

Undefined memory locations should not be written to other
than with the default values suggested in this data sheet. Addresses
that have values marked as 0 should be considered reserved and
have a 0 written into their registers during power-up.


## DEFAULT VALUES

Coming out of reset, critical registers are preloaded with default
values. These values are indicated in Table 12. Other registers
do not have default values and retain the previous value when
exiting reset.


## LOGIC LEVELS

An explanation of various registers follows: "Bit is set" is
synonymous with "bit is set to Logic 1" or "writing Logic 1 for
the bit." Similarly, "clear a bit" is synonymous with "bit is set to
Logic 0" or "writing Logic 0 for the bit."


Table 12. Memory Map Register

| Addr. (Hex) | Register Name | Bit 7 (MSB) | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 (LSB) | Default Value (Hex) | Default Notes/ Comments |
| Chip Configuration Registers | | | | | | | | | |  |  |
| 00 | CHIP_PORT_CONFIG | 0 | LSB first | Soft reset | 1 | 1 | Soft reset | LSB first | 0 | 0x18 | The nibbles should be mirrored by the user so that LSB or MSB first mode registers correctly, regardless of shift mode. |
| 01 | CHIP_ID | 8-bit chip ID, Bits[7:0] = 0x6C | | | | | | | | Read only | Default is a unique chip ID, different for each device. This is a read- only register. |
| 02 | CHIP_GRADE | 0 | 0 | 0 | Speed grade: 00 = 500 MSPS | | X1 ☒ | X1 ☒ | X1 ☒ | Read only | Child ID used to differentiate graded devices. |
| Transfer Register | |  | | | | | | | | | |
| FF | DEVICE_UPDATE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | SW transfer | 0x00 | Synchronously transfers data from the master shift register to the slave. |
| ADC Functions Registers | | | | | | | | | | | |
| 08 | Modes | 0 | 0 | PDWN: 0 = full (default) 1 = standby | 0 | 0 | Internal power-down mode: 000 = normal (power-up, default) 001 = full power-down 010 = standby 011 = normal (power-up) Note that external PDWN pin overrides this setting | | | 0x00 | Determines various generic modes of chip operation. |
| 10 | Offset |  |  | 8-bit | device offset 0111 111 = 0000 0000 1000 0000 = | adjustment +127 codes = 0 codes - 128 codes | [7:0] |  |  | 0x00 | Device offset trim: codes are relative to the output resolution. |
| 0D | TEST_IO | (For mode Bits[3:0] 00 = Pattern 01 = toggle 10 = P1/0000 11 = toggle 0000 | user-defined only, set = 1000) 1 only P1/P2 toggle P1/P2/ | Reset PN23 gen: 1 = on 0 = off (default) | Reset PN9 gen: 1 = on 0 = off (default) | (Format 0100 0111 | determined by Output test mode: 0000 = off (default) 0001 = midscale short 0010 = +FS short 0011 = - FS short = checker board 0101 = PN23 sequence 0110 = PN9 = one/zero word 1000 = user defined 1001 = unused 1010 = unused 1011 = unused 1100 = unused | | OUTPUT_MODE) output toggle | 0x00 | When set, the test data is placed on the output pins in place of normal data. Set pattern values: P1 = Reg 0x19, Reg 0x1A P2 = Reg 0x1B, Reg 0x1C |
|  |
| 0F | AIN_CONFIG | 0 | 0 | 0 | 0 | 0 | Analog input disable: 1 = on 0 = off (default) | 0 | 0 | 0x00 |  |
| 14 | OUTPUT_MODE | 0 | 0 | 0 | Output enable: 0 = enable (default) 1 = disable | 0 | Output invert: 1 = on 0 = off (default) | Data 00 = 01 10 = | format select: offset binary (default) = twos complement Gray code | 0x00 | 0 |
| 15 | OUTPUT_ADJUST | 0 | 0 | 0 | 0 | LVDS course adjust: 0 = 3.5 mA (default) 1 = 2.0 mA | LVDS fine adjust: | | | 0x00 | 0 |
| 001 = 3.50 mA 010 = 3.25 mA 011 = 3.00 mA 100 = 2.75 mA 101 = 2.50 mA 110 = 2.25 mA 111 = 2.00 mA | | |
|  |  |  |
|  |  |  |  |  |
| 16 | OUTPUT_PHASE | Output clock polarity 1 = inverted 0 = normal (default) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0x00 |  |
| 17 | FLEX_OUTPUT_DELAY | 0 | 0 | 0 | 0 |  | Output | clock delay: |  | 0x00 | Shown as |
|  |  | 0000 = 0 0001 = - 1/10 0010 = - 2/10 0011 =- 3/10 0100 = reserved 0101 = +5/10 0110 = +4/10 0111 = +3/10 1000 = +2/10 | | | fractional value of sampling clock period that is subtracted or added to initial tSKEw, see |
|  | Figure 2. |
|  |  |  |
|  |  |  | 1001 = | +1/10 |  |  |  |


AD9484


| Addr. (Hex) | Register Name | Bit 7 (MSB) | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 (LSB) | Default Value (Hex) | Default Notes/ Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 18 | FLEX_VREF | VREF select 00 = internal VREF (20 kQ2 pull-down) 01 = import VREF (0.59 V to 0.8 V on | | 0 |  | Input | voltage range 11100 = 1.60 11101 = 1.58 11110 = 1.55 11111 = 1.52 00000 = 1.50 00001 = 1.47 00010 = 1.44 00011 = 1.42 00100 = 1.39 00101 = 1.36 00110 = 1.34 00111 = 1.31 01000 = 1.28 01001 = 1.26 | setting: |  | 0x00 |  |
|  |
| VREF pin) 10 = export VREF (from internal reference) 11 = not used | |  |  |  |  |
|  |  |  |  |
|  |  | 01010 = 1.23 01011= 1.20 01011= 1.18 |  |  |
| 19 | USER_PATT1_LSB | B7 | B6 | B5 | B4 | B3 | B2 | B1 | B0 | 0x00 | User-defined pattern, 1 LSB. |
| 1A | USER_PATT1_MSB | B7 | B6 | B5 | B4 | B3 | B2 | B1 | B0 | 0x00 | User-defined pattern, 1 MSB. |
| 1B | USER_PATT2_LSB | B7 | B6 | B5 | B4 | B3 | B2 | B1 | B0 | 0x00 | User-defined pattern, 2 LSBs. |
| 1C | USER_PATT2_MSB | B7 | B6 | B5 | B4 | B3 | B2 | B1 | B0 | 0x00 | User-defined pattern, 2 MSBs. |
| 2A | OVR_CONFIG | 0 | 0 | 0 | 0 | 0 | 0 | 0 | OR± enable: 1 = on (default) 0 = off | 0x01 |  |
| 2C | Input coupling | 0 | 0 | 0 | 0 | 0 | DC coupling enable | 0 | 0 | 0x00 | Default is ac coupling. |


1 X = don't care.


# OUTLINE DIMENSIONS


## ORDERING GUIDE


| Model1 | Temperature Range | Package Description | Package Option |
| --- | --- | --- | --- |
| AD9484BCPZ-500 | -40°C to +85°℃ | 56-Lead Lead Frame Chip Scale Package [LFCSP_VQ] | CP-56-5 |
| AD9484BCPZRL7-500 AD9484-500EBZ | -40°C to +85℃ | 56-Lead Lead Frame Chip Scale Package [LFCSP_VQ] Evaluation Board | CP-56-5 |


1 Z = RoHS Compliant Part.


# NOTES
