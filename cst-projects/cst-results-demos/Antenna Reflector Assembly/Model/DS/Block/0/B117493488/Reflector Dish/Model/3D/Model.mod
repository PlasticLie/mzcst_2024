'# MWS Version: Version 2024.0 - Jul 09 2023 - ACIS 33.0.1 -

'# length = m
'# frequency = GHz
'# time = ns
'# frequency range: fmin = 4 fmax = 5
'# created = '[VERSION]2017.0|26.0.1|20161127[/VERSION]


'@ define units

'[VERSION]2017.0|26.0.1|20161205[/VERSION]
With Units 
     .Geometry "m" 
     .Frequency "GHz" 
     .Time "ns" 
     .TemperatureUnit "Kelvin" 
     .Voltage "V" 
     .Current "A" 
     .Resistance "Ohm" 
     .Conductance "Siemens" 
     .Capacitance "PikoF" 
     .Inductance "NanoH" 
End With

'@ change solver type

'[VERSION]2017.0|26.0.1|20161205[/VERSION]
ChangeSolverType "HF IntegralEq"

'@ define background

'[VERSION]2017.0|26.0.1|20161205[/VERSION]
With Background 
     .ResetBackground 
     .XminSpace "0.0" 
     .XmaxSpace "0.0" 
     .YminSpace "0.0" 
     .YmaxSpace "0.0" 
     .ZminSpace "0.0" 
     .ZmaxSpace "0.0" 
     .ApplyInAllDirections "False" 
End With 
With Material 
     .Reset 
     .FrqType "all"
     .Type "Normal"
     .MaterialUnit "Frequency", "Hz"
     .MaterialUnit "Geometry", "m"
     .MaterialUnit "Time", "s"
     .MaterialUnit "Temperature", "Kelvin"
     .Epsilon "1"
     .Mu "1"
     .Sigma "0.0"
     .TanD "0.0"
     .TanDFreq "0.0"
     .TanDGiven "False"
     .TanDModel "ConstSigma"
     .EnableUserConstTanDModelOrderEps "False"
     .ConstTanDModelOrderEps "1"
     .SetElParametricConductivity "False"
     .ReferenceCoordSystem "Global"
     .CoordSystemType "Cartesian"
     .SigmaM "0"
     .TanDM "0.0"
     .TanDMFreq "0.0"
     .TanDMGiven "False"
     .TanDMModel "ConstSigma"
     .EnableUserConstTanDModelOrderMu "False"
     .ConstTanDModelOrderMu "1"
     .SetMagParametricConductivity "False"
     .DispModelEps  "None"
     .DispModelMu "None"
     .DispersiveFittingSchemeEps "Nth Order"
     .MaximalOrderNthModelFitEps "10"
     .ErrorLimitNthModelFitEps "0.1"
     .UseOnlyDataInSimFreqRangeNthModelEps "False"
     .DispersiveFittingSchemeMu "Nth Order"
     .MaximalOrderNthModelFitMu "10"
     .ErrorLimitNthModelFitMu "0.1"
     .UseOnlyDataInSimFreqRangeNthModelMu "False"
     .UseGeneralDispersionEps "False"
     .UseGeneralDispersionMu "False"
     .NonlinearMeasurementError "1e-1"
     .NLAnisotropy "False"
     .NLAStackingFactor "1"
     .NLADirectionX "1"
     .NLADirectionY "0"
     .NLADirectionZ "0"
     .Rho "0"
     .ThermalType "Normal"
     .ThermalConductivity "0"
     .HeatCapacity "0"
     .DynamicViscosity "0"
     .Emissivity "0"
     .MetabolicRate "0"
     .BloodFlow "0"
     .VoxelConvection "0"
     .MechanicsType "Unused"
     .Colour "0.6", "0.6", "0.6" 
     .Wireframe "False" 
     .Reflection "False" 
     .Allowoutline "True" 
     .Transparentoutline "False" 
     .Transparency "0" 
     .ChangeBackgroundMaterial
End With

'@ define boundaries

'[VERSION]2017.0|26.0.1|20161205[/VERSION]
With Boundary
     .Xmin "expanded open"
     .Xmax "expanded open"
     .Ymin "expanded open"
     .Ymax "expanded open"
     .Zmin "expanded open"
     .Zmax "expanded open"
     .Xsymmetry "none"
     .Ysymmetry "none"
     .Zsymmetry "none"
     .ApplyInAllDirections "True"
End With

'@ define frequency range

'[VERSION]2017.0|26.0.1|20161205[/VERSION]
Solver.FrequencyRange "4", "5"

'@ define curve circle: curve1:circle1

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Circle
     .Reset 
     .Name "circle1" 
     .Curve "curve1" 
     .Radius "D/2" 
     .Xcenter "0.0" 
     .Ycenter "0.0" 
     .Segments "0" 
     .Create
End With

'@ transform curve: translate curve1

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Transform 
     .Reset 
     .Name "curve1" 
     .Vector "0", "0", "(D^2)/(16*focus)" 
     .UsePickedPoints "False" 
     .InvertPickedPoints "False" 
     .MultipleObjects "False" 
     .GroupObjects "False" 
     .Repetitions "1" 
     .MultipleSelection "False" 
     .Transform "Curve", "Translate" 
End With

'@ define curve analytical: curve1:analytical1

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With AnalyticalCurve
     .Reset 
     .Name "analytical1" 
     .Curve "curve1" 
     .LawX "t" 
     .LawY "t^2/(4*focus)" 
     .LawZ "0" 
     .ParameterRange "0", "D/2" 
     .Create
End With

'@ transform curve: rotate curve1:analytical1

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Transform 
     .Reset 
     .Name "curve1:analytical1" 
     .Origin "Free" 
     .Center "0", "0", "0" 
     .Angle "90", "0", "0" 
     .MultipleObjects "False" 
     .GroupObjects "False" 
     .Repetitions "1" 
     .MultipleSelection "False" 
     .Transform "Curve", "Rotate" 
End With

'@ new component: component1

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
Component.New "component1"

'@ define sweepprofile: component1:solid1

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With SweepCurve
     .Reset 
     .Name "solid1" 
     .Component "component1" 
     .Material "PEC" 
     .Twistangle "0.0" 
     .Taperangle "0.0" 
     .ProjectProfileToPathAdvanced "False" 
     .DeleteProfile "True" 
     .DeletePath "True" 
     .Path "curve1:circle1" 
     .Curve "curve1:analytical1" 
     .Create
End With

'@ pick point

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
Pick.PickPointFromCoordinates "0", "0", "focus"

'@ define boundaries

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
With Boundary
     .Xmin "expanded open"
     .Xmax "expanded open"
     .Ymin "expanded open"
     .Ymax "expanded open"
     .Zmin "expanded open"
     .Zmax "expanded open"
     .Xsymmetry "magnetic"
     .Ysymmetry "none"
     .Zsymmetry "none"
     .ApplyInAllDirections "False"
End With

'@ define monitor: e-field (f=5)

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
With Monitor 
     .Reset 
     .Name "e-field (f=5)" 
     .Dimension "Volume" 
     .Domain "Frequency" 
     .FieldType "Efield" 
     .MonitorValue "5" 
     .UseSubvolume "False" 
     .Coordinates "Picks" 
     .SetSubvolume "0", "0", "0", "0", "0.3", "0.3" 
     .SetSubvolumeOffset "0.0", "0.0", "0.0", "0.0", "0.0", "0.0" 
     .Create 
End With

'@ define monitor: h-field (f=5)

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
With Monitor 
     .Reset 
     .Name "h-field (f=5)" 
     .Dimension "Volume" 
     .Domain "Frequency" 
     .FieldType "Hfield" 
     .MonitorValue "5" 
     .UseSubvolume "False" 
     .Coordinates "Picks" 
     .SetSubvolume "0", "0", "0", "0", "0.3", "0.3" 
     .SetSubvolumeOffset "0.0", "0.0", "0.0", "0.0", "0.0", "0.0" 
     .Create 
End With

'@ define farfield monitor: farfield (f=5)

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
With Monitor 
     .Reset 
     .Name "farfield (f=5)" 
     .Domain "Frequency" 
     .FieldType "Farfield" 
     .MonitorValue "5" 
     .ExportFarfieldSource "False" 
     .UseSubvolume "False" 
     .Coordinates "Picks" 
     .SetSubvolume "0", "0", "0", "0", "0.3", "0.3" 
     .SetSubvolumeOffset "10", "10", "10", "10", "10", "10" 
     .SetSubvolumeOffsetType "FractionOfWavelength" 
     .Create 
End With

'@ define frequency domain solver parameters

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
Mesh.SetCreator "High Frequency" 
With FDSolver
     .Reset 
     .SetMethod "Surface", "General purpose" 
     .OrderTet "Second" 
     .OrderSrf "First" 
     .Stimulation "List", "List" 
     .ResetExcitationList 
     .AutoNormImpedance "False" 
     .NormingImpedance "50" 
     .ModesOnly "False" 
     .ConsiderPortLossesTet "True" 
     .SetShieldAllPorts "False" 
     .AccuracyHex "1e-6" 
     .AccuracyTet "1e-4" 
     .AccuracySrf "1e-3" 
     .LimitIterations "False" 
     .MaxIterations "0" 
     .SetCalcBlockExcitationsInParallel "True", "True", "" 
     .StoreAllResults "False" 
     .StoreResultsInCache "False" 
     .UseHelmholtzEquation "True" 
     .LowFrequencyStabilization "True" 
     .Type "Iterative" 
     .MeshAdaptionHex "False" 
     .MeshAdaptionTet "True" 
     .AcceleratedRestart "True" 
     .FreqDistAdaptMode "Distributed" 
     .NewIterativeSolver "True" 
     .TDCompatibleMaterials "False" 
     .ExtrudeOpenBC "False" 
     .SetOpenBCTypeHex "Default" 
     .SetOpenBCTypeTet "Default" 
     .AddMonitorSamples "True" 
     .CalcStatBField "False" 
     .CalcPowerLoss "True" 
     .CalcPowerLossPerComponent "False" 
     .StoreSolutionCoefficients "True" 
     .UseDoublePrecision "False" 
     .UseDoublePrecision_ML "True" 
     .MixedOrderSrf "False" 
     .MixedOrderTet "False" 
     .PreconditionerAccuracyIntEq "0.15" 
     .MLFMMAccuracy "Default" 
     .MinMLFMMBoxSize "0.3" 
     .UseCFIEForCPECIntEq "True" 
     .UseFastRCSSweepIntEq "false" 
     .UseSensitivityAnalysis "False" 
     .RemoveAllStopCriteria "Hex"
     .AddStopCriterion "All S-Parameters", "0.01", "2", "Hex", "True"
     .AddStopCriterion "Reflection S-Parameters", "0.01", "2", "Hex", "False"
     .AddStopCriterion "Transmission S-Parameters", "0.01", "2", "Hex", "False"
     .RemoveAllStopCriteria "Tet"
     .AddStopCriterion "All S-Parameters", "0.01", "2", "Tet", "True"
     .AddStopCriterion "Reflection S-Parameters", "0.01", "2", "Tet", "False"
     .AddStopCriterion "Transmission S-Parameters", "0.01", "2", "Tet", "False"
     .AddStopCriterion "All Probes", "0.05", "2", "Tet", "True"
     .RemoveAllStopCriteria "Srf"
     .AddStopCriterion "All S-Parameters", "0.01", "2", "Srf", "True"
     .AddStopCriterion "Reflection S-Parameters", "0.01", "2", "Srf", "False"
     .AddStopCriterion "Transmission S-Parameters", "0.01", "2", "Srf", "False"
     .SweepMinimumSamples "3" 
     .SetNumberOfResultDataSamples "1001" 
     .SetResultDataSamplingMode "Automatic" 
     .SweepWeightEvanescent "1.0" 
     .AccuracyROM "1e-4" 
     .AddInactiveSampleInterval "5", "5", "1", "Single", "False" 
     .MPIParallelization "False"
     .UseDistributedComputing "False"
     .NetworkComputingStrategy "RunRemote"
     .NetworkComputingJobCount "3"
     .UseParallelization "True"
     .MaxCPUs "96"
     .MaximumNumberOfCPUDevices "2"
     .HardwareAcceleration "False"
     .MaximumNumberOfGPUs "1"
End With
With IESolver
     .Reset 
     .UseFastFrequencySweep "False" 
     .UseIEGroundPlane "False" 
     .SetRealGroundMaterialName "" 
     .CalcFarFieldInRealGround "False" 
     .RealGroundModelType "Auto" 
     .PreconditionerType "Auto" 
     .ExtendThinWireModelByWireNubs "False" 
End With
With IESolver
     .SetFMMFFCalcStopLevel "0" 
     .SetFMMFFCalcNumInterpPoints "6" 
     .UseFMMFarfieldCalc "True" 
     .SetCFIEAlpha "0.500000" 
     .LowFrequencyStabilization "False" 
     .LowFrequencyStabilizationML "True" 
     .Multilayer "False" 
     .SetiMoMACC_I "0.0001" 
     .SetiMoMACC_M "0.0001" 
     .DeembedExternalPorts "True" 
     .SetOpenBC_XY "True" 
     .OldRCSSweepDefintion "False" 
     .SetAccuracySetting "Custom" 
     .CalculateSParaforFieldsources "True" 
     .ModeTrackingCMA "True" 
     .NumberOfModesCMA "3" 
     .StartFrequencyCMA "4.000000" 
     .SetAccuracySettingCMA "Default" 
     .FrequencySamplesCMA "0" 
     .SetMemSettingCMA "Auto" 
End With

