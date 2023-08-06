LbEnv
=====

Test scripts for LbLogin prototyping replacement. It defines a stub of
LHCb environment.

BEWARE: It does not overwrite variables already defined, the best is to
try within a session without the LHCb environment (c.f.
${HOME}/.nogrouplogin).

Testing
-------

::

    git clone ssh://git@gitlab.cern.ch:7999/lhcb-core/LbEnv.git
    cd LbEnv 
    export MYSITEROOT=/afs/cern.ch/lhcb/software/rpmrel
    . ./LbEnv.sh

lb-run should now be in the path...

To create the LbEnv.csh:

::

    bin/install.sh

Version installed on AFS
------------------------

You can do directly on lxplus:

::

    bash-4.1$ . /afs/cern.ch/lhcb/software/rpmrel/LbEnv.sh
    bash-4.1$ lb-run DaVinci v37r2p2 gaudirun.py
    # setting LC_ALL to "C"
    ApplicationMgr    SUCCESS 
    ====================================================================================================================================
                                                       Welcome to DaVinci version v37r2p2
                                              running on lxplus0097.cern.ch on Wed Sep  9 18:13:32 2015
    ====================================================================================================================================
    ApplicationMgr       INFO Application Manager Configured successfully
    HistogramPersis...WARNING Histograms saving not required.
    ApplicationMgr       INFO Application Manager Initialized successfully
    ApplicationMgr       INFO Application Manager Started successfully
    EventSelector        INFO End of event input reached.
    EventLoopMgr         INFO No more events in event selection 
    ApplicationMgr       INFO Application Manager Stopped successfully
    EventLoopMgr         INFO Histograms converted successfully according to request.
    ToolSvc              INFO Removing all tools created by ToolSvc
    ApplicationMgr       INFO Application Manager Finalized successfully
    ApplicationMgr       INFO Application Manager Terminated successfully
