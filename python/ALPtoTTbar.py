from HiggsAnalysis.CombinedLimit.PhysicsModel import *

class ALPtoTTbar(PhysicsModel):

    def getYieldScale(self,bin,process):
        if "ALP_ttbar_signal" == process: return "signal_func"
        elif "ALP_ttbar_interference" == process: return "interference_func"
        else:
            return 1

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        self.modelBuilder.doVar("r[1,0,20]");
        self.modelBuilder.doSet("POI", "r")

        self.modelBuilder.factory_("expr::signal_func(\"@0\",r)")
        self.modelBuilder.factory_("expr::interference_func(\"sqrt(@0)\",r)")

alpttottbar = ALPtoTTbar()





# def __init__(self):
#     self.c_G   = 1.0 # gg -> a coupling (default = 1)
#     self.c_Phi = 1.0 # a -> ttbar coupling (default = 1)

# def setPhysicsOptions(self,physOptions):
#     for po in physOptions:
#         if po.startswith("c_G="):
#             self.c_G = float(po.replace("c_G=", ""))
#         if po.startswith("c_Phi="):
#             self.c_Phi = float(po.replace("c_Phi=", ""))

# self.modelBuilder.factory_("expr::C(\"abs(1*1)\")")
# self.modelBuilder.factory_("expr::C(\"abs(@0*@1)\"), c_G, c_Phi")
# self.modelBuilder.factory_("expr::r(\"pow(1.0/pow(@1,2),2)\"), f_a")
