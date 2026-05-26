<figure>

ANALOG
DEVICES

</figure>


# 8-Bit, 500 MSPS, 1.8 V Analog-to-Digital Converter

<!-- PageHeader="AD9484" -->


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


<figure>

VREF

PWDN

AGND

AVDD

REFERENCE

AD9484

CML

DRVDD
DRGND

VIN+

VIN-

TRACK-AND-HOLD

ADC
CORE

8

OUTPUT
STAGING
LVDS

8

D7± TO D0±

CLK+
CLK-

CLOCK
MANAGEMENT

OR+
OR-

SERIAL PORT

DCO+
DCO-

09615-001

SCLK/DFS

SDIO

CSB

Figure 1.

</figure>


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

Information furnished by Analog Devices is believed to be accurate and reliable. However, no
responsibility is assumed by Analog Devices for its use, nor for any infringements of patents or other
rights of third parties that may result from its use. Specifications subject to change without notice. No
license is granted by implication or otherwise under any patent or patent rights of Analog Devices.
Trademarks and registered trademarks are the property of their respective owners.

One Technology Way, P.O. Box 9106, Norwood, MA 02062-9106, U.S.A.
Tel: 781.329.4700

<!-- PageFooter="www.analog.com" -->

Fax: 781.461.3113
@2011 Analog Devices, Inc. All rights reserved.

<!-- PageBreak -->

<!-- PageHeader="AD9484" -->


## TABLE OF CONTENTS


<table>
<tr>
<td>Features</td>
<td>1</td>
</tr>
<tr>
<td>Applications</td>
<td>1</td>
</tr>
<tr>
<td>Functional Block Diagram</td>
<td>1</td>
</tr>
<tr>
<td>General Description</td>
<td>1</td>
</tr>
<tr>
<td>Product Highlights</td>
<td>1</td>
</tr>
<tr>
<td>Revision History</td>
<td>2</td>
</tr>
<tr>
<td>Specifications</td>
<td>3</td>
</tr>
<tr>
<td>DC Specifications</td>
<td>3</td>
</tr>
<tr>
<td>AC Specifications</td>
<td>4</td>
</tr>
<tr>
<td>Digital Specifications</td>
<td>5</td>
</tr>
<tr>
<td>Switching Specifications</td>
<td>6</td>
</tr>
<tr>
<td>Absolute Maximum Ratings.</td>
<td>7</td>
</tr>
<tr>
<td>Thermal Resistance</td>
<td>7</td>
</tr>
<tr>
<td>ESD Caution</td>
<td>7</td>
</tr>
<tr>
<td>Pin Configuration and Function Descriptions</td>
<td>8</td>
</tr>
<tr>
<td>Typical Performance Characteristics</td>
<td>10</td>
</tr>
<tr>
<td>Equivalent Circuits</td>
<td>13</td>
</tr>
<tr>
<td>REVISION HISTORY</td>
<td></td>
</tr>
<tr>
<td>6/11-Rev. 0 to Rev. A</td>
<td></td>
</tr>
<tr>
<td>Change to General Description Section</td>
<td>1</td>
</tr>
<tr>
<td>Change to Aperture Time Parameter in Table 4</td>
<td>6</td>
</tr>
<tr>
<td>Change to Figure 34</td>
<td>16</td>
</tr>
<tr>
<td>Changes to Register 17 and Register 18 in Table 12</td>
<td>20</td>
</tr>
</table>


3/11-Revision 0: Initial Version


<table>
<tr>
<td>Theory of Operation</td>
<td>14</td>
</tr>
<tr>
<td>Analog Input and Voltage Reference</td>
<td>14</td>
</tr>
<tr>
<td>Clock Input Considerations</td>
<td>15</td>
</tr>
<tr>
<td>Power Dissipation and Power-Down Mode</td>
<td>16</td>
</tr>
<tr>
<td>Digital Outputs</td>
<td>16</td>
</tr>
<tr>
<td>Timing</td>
<td>17</td>
</tr>
<tr>
<td>VREF</td>
<td>17</td>
</tr>
<tr>
<td>AD9484 Configuration Using the SPI</td>
<td>18</td>
</tr>
<tr>
<td>Hardware Interface.</td>
<td>18</td>
</tr>
<tr>
<td>Configuration Without the SPI</td>
<td>18</td>
</tr>
<tr>
<td>Memory Map</td>
<td>20</td>
</tr>
<tr>
<td>Reading the Memory Map Table</td>
<td>20</td>
</tr>
<tr>
<td>Reserved Locations</td>
<td>20</td>
</tr>
<tr>
<td>Default Values</td>
<td>20</td>
</tr>
<tr>
<td>Logic Levels</td>
<td>20</td>
</tr>
<tr>
<td>Outline Dimensions</td>
<td>23</td>
</tr>
<tr>
<td>Ordering Guide</td>
<td>23</td>
</tr>
</table>


<!-- PageNumber="Rev. A | Page 2 of 24" -->
