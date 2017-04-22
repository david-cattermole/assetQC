"""
Underlying library of 'assetsQC' tool.

Classes:
- Collector
- Validator
- AssetInstance
- Status
- Fixer
"""

import traceback
import assetQC.api.logger
import assetQC.api.utils
from assetQC.api.status import StatusObject, ErrorStatus, WarningStatus, FailureStatus
import assetQC.api.context as context

# Percentage
START_PERCENT = 0
COLLECTOR_MIN = 1
COLLECTOR_MAX = 29
VALIDATOR_MIN = 30
VALIDATOR_MAX = 59
FIXER_MIN = 60
FIXER_MAX = 79
PROCESS_MIN = 80
PROCESS_MAX = 99
FINISH_PERCENT = 100


def _runCollection(ctx,
                   assetType=None,
                   progressCb=assetQC.api.logger.progress,
                   logger=None):
    if logger is None:
        name = assetQC.api.logger.BASE_LOG_NAME
        logger = assetQC.api.logger.getLogger(name)

    msgBase = 'Collector'
    collectors = ctx.getCollectorPlugins(assetType=assetType)
    numCollectors = len(collectors)

    msg = 'Collectors Found: {num}'.format(num=numCollectors)
    logger.info(msg)

    # loop over collectors and run them.
    for i, collectorObj in enumerate(collectors):
        collector = collectorObj()
        name = collector.getClassName()

        msg = msgBase + ' {name!r}'
        msg = msg.format(name=name)
        assetQC.api.utils.printProgress(msg, i, numCollectors,
                                        COLLECTOR_MIN, COLLECTOR_MAX,
                                        progressCb)

        # do collection
        try:
            collector.doProcess(ctx)
        except WarningStatus, msg:
            collector.logWarning(msg)
        except FailureStatus:
            trace = traceback.format_exc()
            collector.logFailure(trace)
        except AssertionError:
            trace = traceback.format_exc()
            collector.logError(trace)
            raise
        except BaseException:
            trace = traceback.format_exc()
            collector.logError(trace)
            raise
    return ctx


def _runValidation(ctx,
                   assetType=None,
                   progressCb=assetQC.api.logger.progress,
                   logger=None):
    if logger is None:
        name = assetQC.api.logger.BASE_LOG_NAME
        logger = assetQC.api.logger.getLogger(name)

    msgBase = 'Validate'

    instances = ctx.getInstances(sortByName=True)
    numInstances = len(instances)

    msg = 'Asset Instances Found: {num}'.format(num=numInstances)
    logger.info(msg)

    for i, instance in enumerate(instances):
        name = instance.getName()
        aType = instance.getAssetType()

        validators = ctx.getValidatorPlugins(assetType=aType)
        numValidators = len(validators)
        msg = 'Validators Found (for {atype}): {num}'.format(num=numInstances,
                                                         atype=aType)
        logger.info(msg)

        for j, validatorObj in enumerate(validators):
            validator = validatorObj(instance)
            className = validator.getClassName()

            msg = msgBase + ' {assetType} {name!r} {className}'
            msg = msg.format(name=name, assetType=aType, className=className)
            num = i + (float(j) / float(numValidators))
            assetQC.api.utils.printProgress(msg, num, numInstances,
                                            VALIDATOR_MIN, VALIDATOR_MAX,
                                            progressCb)

            # NOTE: instances are assumed valid until proven otherwise.
            try:
                validator.doProcess(ctx)
            except WarningStatus:
                # Users should not raise a warning, instead they should
                # add them to the instance so we can gather as many
                # warnings as possible before returning.
                pass
            except FailureStatus, msg:
                trace = traceback.format_exc()
                instance.logFailure(trace)
                statusObj = StatusObject(FailureStatus,
                                         msg, trace,
                                         validatorObj, validator.fixers)
                instance.addStatus(statusObj)
            except ErrorStatus, msg:
                trace = traceback.format_exc()
                instance.logError(trace)
                statusObj = StatusObject(ErrorStatus,
                                         msg, trace,
                                         validatorObj, validator.fixers)
                instance.addStatus(statusObj)
                raise
            except AssertionError, msg:
                trace = traceback.format_exc()
                instance.logError(trace)
                statusObj = StatusObject(ErrorStatus,
                                         msg, trace,
                                         validatorObj, validator.fixers)
                instance.addStatus(statusObj)
                raise
            except BaseException, msg:
                trace = traceback.format_exc()
                instance.logError(trace)
                statusObj = StatusObject(ErrorStatus, msg, trace,
                                         validatorObj, validator.fixers)
                instance.addStatus(statusObj)
                raise
            else:
                # success!
                pass

                # if not instance.isValid():
                #     instance.addFixers(validatorObj, validator.fixers)

    return ctx


def _runFixers(ctx,
               progressCb=assetQC.api.logger.progress,
               logger=None):
    if logger is None:
        name = assetQC.api.logger.BASE_LOG_NAME
        logger = assetQC.api.logger.getLogger(name)

    msgBase = 'Fixing'

    instances = ctx.getInstances(sortByName=True)
    numInstances = len(instances)
    for i, instance in enumerate(instances):
        name = instance.getName()
        aType = instance.getAssetType()

        statusList = instance.getStatusList()
        numStatus = len(statusList)

        for j, statusObj in enumerate(statusList):
            validatorObj = statusObj.getValidator()
            fixerObjs = statusObj.getFixerList()
            numFixer = len(statusList)
            statusValue = statusObj.getHash()

            for k, fixerObj in enumerate(fixerObjs):
                # run fixer, to try and fix the validation error
                fixer = fixerObj(instance)
                fixerName = fixer.getClassName()

                msg = msgBase + ' {assetType} {name!r} {fixer}'
                msg = msg.format(name=name, assetType=aType, fixer=fixerName)
                num = (float(j + 1) / float(numStatus))
                num *= (float(k + 1) / float(numFixer))
                num += float(i)
                assetQC.api.utils.printProgress(msg, num, numInstances,
                                                FIXER_MIN, FIXER_MAX,
                                                progressCb)

                try:
                    fixer.doProcess(ctx)
                except WarningStatus, msg:
                    pass
                except FailureStatus, msg:
                    trace = traceback.format_exc()
                    instance.logFailure(trace)
                    statusObj = StatusObject(FailureStatus,
                                             msg, trace,
                                             fixerObj, fixerObjs)
                    instance.addStatus(statusObj)
                except AssertionError:
                    trace = traceback.format_exc()
                    instance.logError(trace)
                    statusObj = StatusObject(ErrorStatus,
                                             msg, trace,
                                             fixerObj, fixerObjs)
                    instance.addStatus(statusObj)
                    raise
                except BaseException:
                    trace = traceback.format_exc()
                    instance.logError(trace)
                    statusObj = StatusObject(ErrorStatus,
                                             msg, trace,
                                             fixerObj, fixerObjs)
                    instance.addStatus(statusObj)
                    raise

                # run validator again
                validator = validatorObj(instance)
                try:
                    validator.doProcess(ctx)
                except WarningStatus:
                    pass
                except FailureStatus, msg:
                    trace = traceback.format_exc()
                    instance.logFailure(trace)
                    statusObj = StatusObject(FailureStatus,
                                             msg, trace,
                                             fixerObj, fixerObjs)
                    instance.addStatus(msg)
                    instance.setValid(False)
                except AssertionError:
                    trace = traceback.format_exc()
                    instance.logError(msg)
                    raise
                except BaseException:
                    trace = traceback.format_exc()
                    instance.logError(msg)
                    raise
                else:
                    instance.removeStatus(statusValue)
    return ctx


def _runReporters(ctx,
                  assetType=None,
                  progressCb=assetQC.api.logger.progress,
                  logger=None):
    if logger is None:
        name = assetQC.api.logger.BASE_LOG_NAME
        logger = assetQC.api.logger.getLogger(name)

    msgBase = 'Processing Output'

    reporters = ctx.getReporterPlugins(assetType=assetType)
    numReporters = len(reporters)

    msg = 'Reporters Found: {num}'.format(num=numReporters)
    logger.info(msg)

    for i, reporterObj in enumerate(reporters):
        reporter = reporterObj()
        reporterName = reporter.getClassName()

        msg = msgBase + ' {name}'
        msg = msg.format(name=reporterName)
        assetQC.api.utils.printProgress(msg, i, numReporters,
                                        PROCESS_MIN, PROCESS_MAX,
                                        progressCb)

        # do reporter
        try:
            reporter.doProcess(ctx)
        except WarningStatus, msg:
            reporter.logWarning(msg)
        except FailureStatus:
            trace = traceback.format_exc()
            reporter.logFailure(trace)
        except AssertionError:
            trace = traceback.format_exc()
            reporter.logError(trace)
            raise
        except BaseException:
            trace = traceback.format_exc()
            reporter.logError(trace)
            raise
    return ctx


def run(ctx=None,
        assetType=None,
        doCollectors=True,
        doValidators=True,
        doFixers=True,
        doReporters=True,
        logger=None,
        progressCb=assetQC.api.logger.progress):
    """
    Runs asset quality checking.

    :param ctx:
    :param assetType:
    :param doCollectors:
    :param doValidators:
    :param doFixers:
    :param doReporters:
    :param logger:
    :param progressCb: Progress Callback
    
    :type ctx: assetQC.api.context.Context
    :type assetType: str
    :type doCollectors: bool
    :type doValidators: bool
    :type doFixers: bool
    :type doReporters: bool
    :type logger: assetQC.api_tests.logger.Logger
    :type progressCb: function
    :return:
    """
    msg = 'Initializing Context...'
    assetQC.api.utils.printProgressNum(msg, START_PERCENT,
                                       progressCb,
                                       logger=logger)
    if not ctx:
        ctx = context.Context()
    assert isinstance(ctx, context.Context)

    # collectors step.
    if doCollectors:
        msg = 'Running Collectors...'
        assetQC.api.utils.printProgressNum(msg, COLLECTOR_MIN,
                                           progressCb,
                                           logger=logger)
        ctx = _runCollection(ctx,
                             assetType=assetType,
                             progressCb=progressCb,
                             logger=logger)
        if not ctx.getInstances(sortByName=True):
            msg = 'Cannot find any instances: {instances!r}'
            msg = msg.format(instances=ctx.getInstances(sortByName=True))
            assetQC.api.logger.warning(msg,
                                       logger=logger)

            msg = 'Finished Asset QC'
            assetQC.api.utils.printProgressNum(msg, FINISH_PERCENT,
                                               progressCb,
                                               logger=logger)
            return

    # validators step
    if doCollectors and doValidators:
        msg = 'Running Validators...'
        assetQC.api.utils.printProgressNum(msg, VALIDATOR_MIN,
                                           progressCb,
                                           logger=logger)
        ctx = _runValidation(ctx,
                             assetType=assetType,
                             progressCb=progressCb)

    # fixers step.
    if doCollectors and doValidators and doFixers:
        msg = 'Running Fixers...'
        assetQC.api.utils.printProgressNum(msg, FIXER_MIN,
                                           progressCb,
                                           logger=logger)
        ctx = _runFixers(ctx,
                         progressCb=progressCb)

    # reporter step.
    if doCollectors and doValidators and doReporters:
        msg = 'Report Output...'
        assetQC.api.utils.printProgressNum(msg, PROCESS_MIN,
                                           progressCb,
                                           logger=logger)
        _runReporters(ctx,
                      assetType=assetType,
                      progressCb=progressCb)

    msg = 'Finished Asset QC'
    assetQC.api.utils.printProgressNum(msg, FINISH_PERCENT,
                                       progressCb,
                                       logger=logger)
