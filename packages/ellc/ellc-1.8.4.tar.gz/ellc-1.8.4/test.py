import ellc
import numpy as np
import matplotlib.pyplot as plt
t = np.arange(-0.25,0.75, 0.00001)
spots_1 = [[30,180],[45,-45],[25,35],[0.2,0.8]]

flux = ellc.lc(t,radius_1=0.1,radius_2=0.05,sbratio=0.2, \
               incl=89.95,q=0.5,ld_1='quad',ldc_1=[0.65,0.2],ld_2='lin',ldc_2=0.45,
               shape_1='poly3p0',shape_2='poly1p5',spots_1=spots_1, verbose=False)

flux1, flux2 = ellc.fluxes(t,radius_1=0.1,radius_2=0.05,sbratio=0.2, \
                        incl=89.95,q=0.5,ld_1='quad',ldc_1=[0.65,0.2],ld_2='lin',ldc_2=0.45,
                        shape_1='poly3p0',shape_2='poly1p5',spots_1=spots_1, verbose=False)

plt.figure(figsize=(10,6))
plt.plot(t,flux1, label='flux1, unscaled (fluxes.py)')
plt.plot(t,flux2, label='flux2, unscaled (fluxes.py)')
plt.plot(t,flux1+flux2, label='flux1+2, unscaled (fluxes.py)')
plt.legend()
plt.show()

plt.figure(figsize=(10,6))
plt.plot(t,flux, label='total flux (lc.py)')
plt.plot(t,flux1+flux2, label='flux1+2, scaled (fluxes.py)')
plt.legend()
plt.show()

plt.figure(figsize=(10,6))
plt.plot(t,flux1, label='flux1, scaled (fluxes.py)')
plt.plot(t,flux2, label='flux2, scaled (fluxes.py)')
plt.plot(t,flux1+flux2, label='flux1+2, scaled (fluxes.py)')
plt.legend()
plt.show()
