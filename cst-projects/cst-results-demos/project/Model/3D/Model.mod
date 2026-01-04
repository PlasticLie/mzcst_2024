'# MWS Version: Version 2024.5 - Jun 14 2024 - ACIS 33.0.1 -

'# length = mm
'# frequency = GHz
'# time = ns
'# frequency range: fmin = 8 fmax = 10
'# created = '[VERSION]2024.5|33.0.1|20240614[/VERSION]


'@ define frequency range

'[VERSION]2024.5|33.0.1|20240614[/VERSION]
Solver.FrequencyRange 8, 10

'@ define monitor: e-field (f=9)

'[VERSION]2024.5|33.0.1|20240614[/VERSION]
With Monitor
     .Reset
     .Name "e-field (f=9)"
     .Dimension "Volume"
     .Domain "Frequency"
     .FieldType "Efield"
     .Frequency 9
     .Create
End With

'@ define solver parameters

'[VERSION]2024.5|33.0.1|20240614[/VERSION]
With Solver
     .CalculationType "TD-S"
     .StimulationPort "1"
     .StimulationMode "1"
     .MeshAdaption False
     .CalculateModesOnly False
     .SParaSymmetry False
     .StoreTDResultsInCache False
     .FullDeembedding False
     .UseDistributedComputing False
End With

'@ define special solver parameters

'[VERSION]2024.5|33.0.1|20240614[/VERSION]
With Solver
     .AdaptivePortMeshing False
End With

'@ execute macro: Construct\Demo Examples\Waveguide T-Splitter

'[VERSION]2024.5|33.0.1|20240614[/VERSION]
'  execute macro: File / Set My Defaults

'  define units 

With Units
     .Geometry "mm" 
     .Frequency "ghz" 
     .Time "ns" 
End With 

'  set workplane properties

With WCS
     .SetWorkplaneSize "50" 
     .SetWorkplaneRaster "10"
     .SetWorkplaneSnap "TRUE" 
     .SetWorkplaneSnapRaster "5"
End With

'  new component: component1
Component.New "component1" 

'  define brick: component1:solid1
With Brick
     .Reset 
     .Name "solid1" 
     .Component "component1" 
     .Material "Vacuum" 
     .Xrange "-10", "10" 
     .Yrange "0", "10" 
     .Zrange "0", "40" 
     .Create
End With

'  pick face
Pick.PickFaceFromId "component1:solid1", "6" 

'  align wcs with face
WCS.AlignWCSWithSelectedFace 
Pick.PickCenterpointFromId "component1:solid1", "6" 
WCS.AlignWCSWithSelectedPoint 

'  define brick: component1:solid2
With Brick
     .Reset 
     .Name "solid2" 
     .Component "component1" 
     .Material "Vacuum" 
     .Xrange "-5", "5" 
     .Yrange "-10", "10" 
     .Zrange "0", "20" 
     .Create
End With

'  pick face
Pick.PickFaceFromId "component1:solid2", "1" 

'  define port: 1
With Port 
     .Reset 
     .PortNumber "1" 
     .NumberOfModes "1" 
     .AdjustPolarization False 
     .PolarizationAngle "0.0" 
     .ReferencePlaneDistance "0" 
     .TextSize "50" 
     .Coordinates "Picks" 
     .Orientation "xmax" 
     .PortOnBound "True" 
     .ClipPickedPortToBound "False" 
     .Xrange "30", "30" 
     .Yrange "0", "10" 
     .Zrange "10", "30" 
     .Create 
End With 

'  pick face
Pick.PickFaceFromId "component1:solid1", "1" 

'  define port: 2
With Port 
     .Reset 
     .PortNumber "2" 
     .NumberOfModes "1" 
     .AdjustPolarization False 
     .PolarizationAngle "0.0" 
     .ReferencePlaneDistance "0" 
     .TextSize "50" 
     .Coordinates "Picks" 
     .Orientation "zmax" 
     .PortOnBound "True" 
     .ClipPickedPortToBound "False" 
     .Xrange "-10", "10" 
     .Yrange "0", "10" 
     .Zrange "40", "40" 
     .Create 
End With 

'  pick face
Pick.PickFaceFromId "component1:solid1", "2" 

'  define port: 3
With Port 
     .Reset 
     .PortNumber "3" 
     .NumberOfModes "1" 
     .AdjustPolarization False 
     .PolarizationAngle "0.0" 
     .ReferencePlaneDistance "0" 
     .TextSize "50" 
     .Coordinates "Picks" 
     .Orientation "zmin" 
     .PortOnBound "True" 
     .ClipPickedPortToBound "False" 
     .Xrange "-10", "10" 
     .Yrange "0", "10" 
     .Zrange "0", "0" 
     .Create 
End With 

'  define boundaries
With Boundary
     .Xmin "electric" 
     .Xmax "electric" 
     .Ymin "electric" 
     .Ymax "electric" 
     .Zmin "electric" 
     .Zmax "electric" 
     .Xsymmetry "none" 
     .Ysymmetry "electric" 
     .Zsymmetry "none" 
End With

'  define background
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
     .Type "Pec"
     .MaterialUnit "Frequency", "Hz"
     .MaterialUnit "Geometry", "m"
     .MaterialUnit "Time", "s"
     .MaterialUnit "Temperature", "Kelvin"
     .Epsilon "1.0"
     .Mu "1.0"
     .ReferenceCoordSystem "Global"
     .CoordSystemType "Cartesian"
     .NLAnisotropy "False"
     .NLAStackingFactor "1"
     .NLADirectionX "1"
     .NLADirectionY "0"
     .NLADirectionZ "0"
     .Rho "0.0"
     .ThermalType "Normal"
     .ThermalConductivity "0.0"
     .SpecificHeat "0.0", "J/K/kg"
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

'  activate global coordinates
WCS.ActivateWCS "global"

'  boolean add shapes: component1:solid1, component1:solid2
Solid.Add "component1:solid1", "component1:solid2" 

'  pick face
Pick.PickFaceFromId "component1:solid1", "11" 

'  align wcs with face
WCS.AlignWCSWithSelectedFace 
Pick.PickCenterpointFromId "component1:solid1", "11" 
WCS.AlignWCSWithSelectedPoint 

'  store picked point: 1
Pick.NextPickToDatabase "1" 
Pick.PickEndpointFromId "component1:solid1", "9"


'  define cylinder: component1:solid2
With Cylinder 
     .Reset 
     .Name "solid2" 
     .Component "component1" 
     .Material "PEC" 
     .OuterRadius "1" 
     .InnerRadius "0" 
     .Axis "z" 
     .Zrange "zp(1)", "0" 
     .Xcenter "-10+offset"
     .Ycenter "0" 
     .Segments "0" 
     .Create 
End With 

'  activate global coordinates
WCS.ActivateWCS "global"

'@ define time domain solver parameters

'[VERSION]2024.5|33.0.1|20240614[/VERSION]
Mesh.SetCreator "High Frequency" 

With Solver 
     .Method "Hexahedral"
     .CalculationType "TD-S"
     .StimulationPort "1"
     .StimulationMode "1"
     .SteadyStateLimit "-40"
     .MeshAdaption "False"
     .CalculateModesOnly "False"
     .SParaSymmetry "False"
     .StoreTDResultsInCache  "False"
     .RunDiscretizerOnly "False"
     .FullDeembedding "False"
     .SuperimposePLWExcitation "False"
     .UseSensitivityAnalysis "False"
End With

'@ set PBA version

'[VERSION]2024.5|33.0.1|20240614[/VERSION]
Discretizer.PBAVersion "2024061424"

'@ change solver type

'[VERSION]2024.5|33.0.1|20240614[/VERSION]
ChangeSolverType "HF Time Domain"

