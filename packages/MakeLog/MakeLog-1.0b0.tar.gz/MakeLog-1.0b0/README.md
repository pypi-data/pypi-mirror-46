# **MakeLog**
![GitHub issues](https://img.shields.io/github/issues/darryllane/MakeLog.svg)


**Essentials**
---
[![Python 3.4](https://img.shields.io/badge/python-3.4%20+-green.svg)](https://www.python.org/downloads/release/python-360/) ![GitHub](https://img.shields.io/github/license/darryllane/MakeLog.svg)
---
Simple logger for info, error and debug logs.

**Testing**
---
[![Coverage Status](https://coveralls.io/repos/github/darryllane/MakeLog/badge.svg?branch=master)](https://coveralls.io/github/darryllane/MakeLog?branch=master) [![Build Status](https://travis-ci.org/darryllane/MakeLog.svg?branch=master)](https://travis-ci.org/darryllane/MakeLog)

**Example**
---

    # import library
    from MakeLog import make_log as log
    
    # initialse Class
    logger = log.initialise()
    
    # write info log
    logger.info('info_test')
    
    # write error log
    logger.error('error_test')
    
    # write debug log
    logger.debug('debug_test')

**Features**
---
Takes Log directory input (not required)

Takes log filename inputs (not required)