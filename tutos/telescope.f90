program telescope

use optocad
use rsplot

character(len=160)	:: ocd(10)=''
wl=1.064e-6		!light wavelength (in mm)


ocd(01) = ' '

ocd(02)='b 0.0, 0.0, .005, 0.0, z=0.'

ocd(03)='d srt, 1., 0., 0.025, ag=-5.710593137599527, c = 0.9, r = 0.5'
ocd(04) = '+ t, da = 0.2, r = 0.1'

ocd(05)='d srt, 0., 0.2, 0.025, ag= 174.2894068624005, c = 0.9, r = 0.5'
ocd(06)='+ t, da = 0.2, r = 0.1'
call oc_init(unit='m')! Initialize OPTOCAD (A4 landscape)

call oc_frame(-0.1,-0.1, 1.20, 0.30 ,glp=0, scale = 0.2)! Set up a frame

call oc_set(pctl=1, part=1, &
		print='rs s2 Act ang z1t w0t z0t  w1t R1t')

call oc_input(ocd)	! This reads the data of the components.
call oc_trace		! Trace all ray segments


call oc_beam(0.0,1,5,.2)	! Plot beam axes and numbers in black

call oc_surf(lw=.3)! Plot all surfaces with linewidth 0.3mm
				! ... and surface numbers in magenta
call oc_exit
end
