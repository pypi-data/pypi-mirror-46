# Rohde&Schwarz Python SCPI Driver

## Description

- Example python drivers
  - FSW, Vector Spectrum Analyzer
  - SMW, Vector Signal Generator
  - NRP, Power Sensor
  - VSE, Vector Signal Explorer
  - VST, Vectro Signal Transciever (Calls to FSW & SMW)
  - OSP, Switch Driver
  - NRQ, Frequency Selective Power Sensor

- Example code
  - Automated test examples (see below table)
  - Instrument speed/repeatability evaluation
  - Proof of concept/Demo code

- RSSD is in development
  - Package APIs **may*- change.
  - We recommend users "freeze/save" package version prior to use.
  - SW is provided as is

## Getting Started

### Installation

```python
python -m pip install rssd
```

### Running

- Load example files in &lt;Python Install Directory&gt;\Lib\site-packages\rssd\examples

    ```python
    python -m pip show rssd
    ```

- Change IP address to match instrument(s)
- Run

### Example Code

FileName                | Instrumnt | Description                        |
------------------------|-----------|------------------------------------|
[AAA_CommandTime](https://github.com/mclim9/rssd/blob/master/rssd/examples/)         | Any       | Time command to instrument         |
[AAA_IDN_IPArry](https://github.com/mclim9/rssd/blob/master/rssd/examples/)          | Any       | Send *IDN to instruments in IPArry |
[FSW_ACLR_Timing](https://github.com/mclim9/rssd/blob/master/rssd/examples/)         | VSA       | ACLR in Spectral Mode              |
[FSW_ACLR_IQ_Timing](https://github.com/mclim9/rssd/blob/master/rssd/examples/)      | VSA       | ACLR in IQ Analyzer                |
[FSW_CCDF](https://github.com/mclim9/rssd/blob/master/rssd/examples/)                | VSA       | CCDF in Spectral Mode              |
[FSW_IQCaptureTime](https://github.com/mclim9/rssd/blob/master/rssd/examples/)       | VSA       | IQ Capture time looping Fs         |
[NRP_AvGPwr](https://github.com/mclim9/rssd/blob/master/rssd/examples/)              | NRP       | NRP Average power capture          |
[NRP_BufferedContAvg](https://github.com/mclim9/rssd/blob/master/rssd/examples/)     | NRP       | Bufferened NRP measurement         |
[SMW_LoadArb.py](https://github.com/mclim9/rssd/blob/master/rssd/examples/)          | VSG       | Load Arb file into SMW             |
[OSP_Debug](https://github.com/mclim9/rssd/blob/master/rssd/examples/)               | OSP       | Generic OSP example                |
[VSE_ADemod.py](https://github.com/mclim9/rssd/blob/master/rssd/examples/)           | VSE       | VSE/FSW Analog FM Demod            |
[VSE_Debug.py](https://github.com/mclim9/rssd/blob/master/rssd/examples/)            | VSE       | VSE Raw SCPI                       |
[VSE_OFDM_1CC_K96.py](https://github.com/mclim9/rssd/blob/master/rssd/examples/)     | VSE       | VSE Single OFDM Carrier EVM w/ K96 |
[VSE_OFDM_MultiCC_K96.py](https://github.com/mclim9/rssd/blob/master/rssd/examples/) | VSE       | VSE Multi  OFDM Carrier EVM w/ K96 |
[VST_5GNR_EVM](https://github.com/mclim9/rssd/blob/master/rssd/examples/)            | VSG VSA   | SMW/FSW K144 speed tests           |
[VST_5GNR_K144_Read](https://github.com/mclim9/rssd/blob/master/rssd/examples/)      | VSG VSA   | SMW/FSW Read 5G NR Parametes       |
[VST_Sweep.py](https://github.com/mclim9/rssd/blob/master/rssd/examples/)            | VSG VSA   | SMW/FSW Frequency Sweep            |
[VST_WLAN_EVM](https://github.com/mclim9/rssd/blob/master/rssd/examples/)            | VSG VSA   | SMW/FSW 802.11 EVM sweep test      |

# Documentation

## Driver Structure

- Driver Structure:
  - Common Driver Call: pyvisa &rarr; yaVISA.py &rarr; &lt;**instr**&gt;\_Common.py &rarr;
  - Instrument Options: pyvisa &rarr; yaVISA.py &rarr; &lt;**instr**&gt;\_Common.py &rarr; &lt;**instr**&gt;\_&lt;OptionName&gt;\_Kxx.py
- yaVISA: pyvisa wrapper
  - **yaVISA.jav_Open(sFileName, sLogFile)**: Open VISA link
  - **yaVISA.write(sSCPI)**: Write SCPI command
  - **yaVISA.query(sSCPI)**: Query SCPI command
  - **yaVISA.jav_logscpi()**: Turn on "SCPI to file"
  - **yaVISA.jav_OPC_Wait(sCmd)**: Wait for longer commands.
  - Please see **yaVISA.py*- for full list of commands.

## Specific Instrument Drivers

- FSW: Vector Spectrum Analyzer
  - Developed & Tested with FSW
  - FSW & VSE share many commands.
  - Possible compatibility: VSE; FPS; FSV;
- SMW: Vector Signal Generator
  - Developed & Tested with SMW
  - Possible compatibility: SGS; SGT; SMB; SMBV
- NRP: Power Sensor
  - Developed & Tested with NRPxxS/SN sensors
- VSE: Vector Signal Explorer SW
  - Developed & Tested with VSE
  - Drivers represent VSE commands not in FSW code
  - OFDMVSA K96 code resides here as well
  - Possible compatibility: FSW
- VST: Vector Signal Transceiver
  - Code that calls both SMW & FSW
  - Currently 5GNR; LTE; WLAN implemented
- OSP: Open Switch and Control Platform
  - Developed & Tested with OSP120

## Instrument Documentation

Driver     | Description | User Manual | Models
-----------|-------------|-------------|--------------
SMW | Vector Signal Generator   | [User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=smw+vector+user+manual&sort=relevance) | [SMW](https://www.rohde-schwarz.com/us/product/smw200a); [SMBV](https://www.rohde-schwarz.com/us/product/smbv100b); [SGT](https://www.rohde-schwarz.com/us/product/sgt100A); [SGS](https://www.rohde-schwarz.com/us/product/sgs100A); [SMA-B](https://www.rohde-schwarz.com/us/product/sma100b); [SMB-B](https://www.rohde-schwarz.com/us/product/smb100b); [SMF](https://www.rohde-schwarz.com/us/product/smf100a) |
FSW | Vector Signal Analyzer    | [User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=FSW+user+manual&sort=relevance) | [FSW](https://www.rohde-schwarz.com/us/product/fsw); [FSWP](https://www.rohde-schwarz.com/us/product/fswp); [FSVA](https://www.rohde-schwarz.com/us/product/fsva); [FPL](https://www.rohde-schwarz.com/us/product/fpl1000);
VSE | Vector Analysis Software  | [User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=vse+base+user+manual) | [VSE](https://www.rohde-schwarz.com/us/product/vse)
CMW | Basestation Emulator      | [User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=cmw+user+manual) | [CMW500](https://www.rohde-schwarz.com/us/product/CMW500); [CMW100](https://www.rohde-schwarz.com/us/product/CMW100); [CMP200](https://www.rohde-schwarz.com/us/product/CMP200)
NRP | Three Path Power Sensor   | [User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=nrp_s_sn+user+manual) | [NRP](https://www.rohde-schwarz.com/us/product/nrp_s_sn); [NRPM](https://www.rohde-schwarz.com/us/product/nrpm)
NRQ | Freq Selective Pwr Sensor | [User Manual](https://www.rohde-schwarz.com/us/manual/nrq6/) | [NRQ](https://www.rohde-schwarz.com/us/product/nrq6)
OSP | Switch Matrix             | [User Manual](https://www.rohde-schwarz.com/us/manual/osp/) | [OPS1xx](https://www.rohde-schwarz.com/us/product/osp); [OPS2xx](https://www.rohde-schwarz.com/us/product/osp-n)
VNA | Network Analyzer          | [User Manual](https://www.rohde-schwarz.com/us/manual/zva/) | [ZVA](https://www.rohde-schwarz.com/us/product/zva); [ZNA](https://www.rohde-schwarz.com/us/product/zna); [ZNB](https://www.rohde-schwarz.com/us/product/ZNB)
[N/A] | Digital Oscillocope       | [User Manual](https://www.rohde-schwarz.com/us/manual/rtp/) | [RTP](https://www.rohde-schwarz.com/us/product/RTP); [RTO](https://www.rohde-schwarz.com/us/product/RTO);
[N/A] | Radiated Chambers         | [User Manual](https://www.rohde-schwarz.com/us/manual/ATS1000/) |[ATS800](https://www.rohde-schwarz.com/us/product/ATS800); [ATS1000](https://www.rohde-schwarz.com/us/product/ATS1000); [ATS1800](https://www.rohde-schwarz.com/us/product/ATS1800); [CMQ](https://www.rohde-schwarz.com/us/product/CMQ100); [DST200](https://www.rohde-schwarz.com/us/product/DST200); [TS7124](https://www.rohde-schwarz.com/us/product/ts7124)

# Project

- Code Repository: [GitHub](https://github.com/mclim9/rssd)
- Author: Martin C Lim
- License: This project is licensed under the R&S License for Royalty-Free Products- see the [LICENSE](LICENSE.txt) file for details

## Acknowledgments

- Thanx to [Nick Lalic](https://pypi.org/project/rohdeschwarz/) for all his help.
- [Markdown reference](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)