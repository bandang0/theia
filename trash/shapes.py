ap = lens.apexes()
    Cyl = Part.makeCylinder((lens.Dia/2.)/fact, max(lens.Thick/fact, 0.01/fact),
                                 Base.Vector(0,0,0),
                                 Base.Vector(tuple(-lens.HRNorm)))

    Cone1 = Part.makeCone(0., lens.Dia/2./fact,
                            np.linalg.norm(ap[0] - lens.HRCenter)/fact,
                            Base.Vector(tuple(ap[0]/fact - lens.HRCenter/fact)),
                            Base.Vector(tuple(-lens.HRCenter)))

    Cone2 = Part.makeCone(0., lens.Dia/2./fact,
                            np.linalg.norm(ap[1] - lens.ARCenter)/fact,
                            Base.Vector(tuple(ap[1]/fact - lens.HRCenter/fact)),
                            Base.Vector(tuple(-lens.ARCenter)))
    print lens.ARCenter
    print lens.HRCenter
    print lens.HRK
    print lens.ARK
    return Cone1.fuse(Cone2)
    if lens.HRK > 0.:
        rtn =  Cyl.cut(Cone1)
    else:
        rtn = Cyl.fuse(Cone1)

    if lens.ARK > 0.:
        return rtn.cut(Cone2)
    else:
        return rtn.fuse(Cone2)
