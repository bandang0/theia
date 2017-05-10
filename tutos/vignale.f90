program telescope

use optocad
use rsplot

character(len=160)	:: ocd(10)=''
wl=1.064e-6		!light wavelength (in mm)


ocd(01) = ' '

ocd(02)='b 0.0, 0.0, .001, 0.0, z=0.'

ocd(03)='c r, .1, 0., 0.05, ag=-5.710593137599527, c = -10., r = 0.5'

call oc_init(unit='m')! Initialize OPTOCAD (A4 landscape)

call oc_frame(-0.1,-0.1, .2, 0.10 ,glp=0, scale = 0.4)! Set up a frame

call oc_set(pctl=1, part=1, &
		print='rs s2 Act ang z1t w0t z0t  w1t R1t')

call oc_input(ocd)	! This reads the data of the components.
call oc_trace	! Trace all ray segments


call oc_beam(0.0,1,5,.2)	! Plot beam axes and numbers in black

call oc_surf(lw=.3)! Plot all surfaces with linewidth 0.3mm
				! ... and surface numbers in magenta
call oc_exit
end
