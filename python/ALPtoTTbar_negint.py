from HiggsAnalysis.CombinedLimit.PhysicsModel import *

class ALPtoTTbar_negint(PhysicsModel):

    def getYieldScale(self,bin,process):
        if "ALP_ttbar_signal" == process:
            return "signal_func"
        elif "ALP_ttbar_interference" == process:
            return "interference_func"
        else:
            return 1

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        self.modelBuilder.doVar("r[1,0,20]")
        self.modelBuilder.doSet("POI", "r")

        self.modelBuilder.factory_("expr::signal_func(\"@0**2\",r)")
        self.modelBuilder.factory_("expr::interference_func(\"-@0\",r)")

alptottbar_negint = ALPtoTTbar_negint()
