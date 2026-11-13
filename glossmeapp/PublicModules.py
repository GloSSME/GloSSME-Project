from   glossme.PublicFunctions      import      *


def fnGetCommonValues(      nLanguageID             =   1
                        ,   nCommonValueCategoryID  =   None
                    ):

    tuParameters    =   []

    cStrSQL     =   """
                        SELECT
                                    [nCommonValuesMasterID]     -- 0
                                ,   [nLanguageID]               -- 1
                                ,   [cCommonValueName]          -- 2
                                ,   [nCommonValueCategoryID]    -- 3
                        FROM        [ViewCommonValues]
                        WHERE       1   =   1
                    """

    if int(nLanguageID)     >   0:
        cStrSQL         +=  "   AND   nLanguageID   =   %s"
        tuParameters.append(nLanguageID)

  
    if nCommonValueCategoryID is not None:
        cStrSQL         +=  "   AND   nCommonValueCategoryID   =   %s"
        tuParameters.append(nCommonValueCategoryID)

    cStrSQL             +=  "   ORDER BY     cCommonValueName"
    tuParameters        =   tuple(tuParameters)

    dtResult            =   fnPublicFetchAll(       cStrSQL
                                                ,   tuParameters
                                                ,   'default'
                                            )

    if dtResult:
        lstResult   =   [
                        {       'nCommonValuesMasterID'     :   dtValue[0]
                            ,   'nLanguageID'               :   dtValue[1]
                            ,   'cCommenValueName'          :   dtValue[2]
                            ,   'nCommonValueCategoryID'    :   dtValue[3]
                        }       for dtValue in dtResult
                    ]
        return lstResult
    else:
        return None