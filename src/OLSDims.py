class AppDim:
    AppOLS = [
          #[i][0]=OuterHor #[i][1]=Con #[i][2]=InHor  #[i][3]=App                                   #[i][4]=InApp        #[i][5]=Trans #[i][6]=InTrans  #[i][7]=BaulkedLand
          [[0,0],          [.05,35],   [45,2000], [60, 30,.1, 1600,.05,   0,    0,  0  ,    1600],  [0,   0,  0,    0],    [.2],       [0],            [0,  0,    0,0   ]], #AppOLS[0] = non-instrument CN1
          [[0,0],          [.05,55],   [45,2500], [80, 60,.1, 2500,.04,   0,    0 ,   0 ,    2500], [0,   0,  0,    0],    [.2],       [0],            [0,  0,    0,0   ]], #AppOLS[1] = non-instrument CN2
          [[0,0],          [.05,75],   [45,4000], [150,60,.1, 3000,.0333, 0,    0 ,  0  ,    3000], [0,   0,  0,    0],    [.143],     [0],            [0,  0,    0,0   ]], #AppOLS[2] = non-instrument CN3
          [[0,0],          [.05,100],  [45,4000], [150,60,.1, 3000,.025, 0 ,    0 ,  0  ,    3000], [0,   0,  0,    0],    [.143],     [0],            [0,  0,    0,0   ]], #AppOLS[3] = non-instrument CN4
          ## updated numbers in new regs started in september 2019 for approach instrument non precision
          [[0,0],          [.05,60],   [45,3500], [140,60,.15,2500,.0333,0 ,    0 ,  0  ,    2500], [0,   0,  0,    0],    [.2],       [0],            [0,  0,    0,0   ]], #AppOLS[4] = INP CN1,2
          [[0,0],          [.05,75],   [45,4000], [280,60,.15,3000,.02,   3600, .025,8400,15000],   [0,   0,  0,    0],    [.143],     [0],            [0,  0,    0,0   ]], #AppOLS[5] = INP CN3
          [[0,0],          [.05,100],  [45,4000], [280,60,.15,3000,.02,   3600, .025,8400,15000],   [0,   0,  0,    0],    [.143],     [0],            [0,  0,    0,0   ]], #AppOLS[6] = INP CN4
          [[0,0],          [.05,60],   [45,3500], [140,60,.15,3000,.025,  12000,.03 ,0 ,    15000], [90, 60,900,0.025],    [.143],     [.40],          [90, 0,   .1,0.04]], #AppOLS[7] = PA1 CN1,2
          [[150,15000],    [.05,100],  [45,4000], [280,60,.15,3000,.02,   3600, .025,8400,15000],   [120,60,900, 0.02],    [.143],     [.333],         [120,1800,.1,0.033]], #AppOLS[8] = PAI CN3,4
          [[150,15000],    [.05,100],  [45,4000], [280,60,.15,3000,.02,   3600, .025,8400,15000],   [120,60,900, 0.02],    [.143],     [.333],         [120,1800,.1,0.033]], #AppOLS[9] = PAII, III CN3,4
          ]

    AppOLSNAME = ['OUTER HORIZONTAL','CONICAL','INNER HORIZONTAL','APPROACH','INNER APPROACH','TRANSITIONAL','INNER TRANSITIONAL','BAULKED LANDING']
    AppOLSDIMS = [  #OUTER HORIZONTAL,
                    ['Height (m)',
                    'Radius (m)'],
                    #CONICAL,
                   [ 'Slope',
                    'Height (m)'],
                    #INNER HORIZONTAL,
                    ['Height (m)',
                    'Radius (m)'],
                    #APPROACH,
                    ['Length of inner edge (m)',
                    'Distance from threshold (m)',
                    'Divergence each side',
                    'First section length (m)',
                    'Slope',
                    'Second section length (m)',
                    'Slope',
                    'Horizontal section length (m)',
                    'Total length (m)'],
                    #INNER APPROACH,
                    ['Width (m)',
                    'Distance from threshold (m)',
                    'Length (m)',
                    'Slope'],
                    #TRANSITIONAL,
                    ['Slope'],
                    #INNER TRANSITIONAL,
                    ['Slope'],
                    #BAULKED LANDING,
                    ['Length of inner edge (m)',
                    'Distance from threshold (m)',
                    'Divergence each side',
                    'Slope']
                    ]
    AppOLS_old = [
          #[i][0]=OuterHor #[i][1]=Con #[i][2]=InHor  #[i][3]=App                                   #[i][4]=InApp        #[i][5]=Trans #[i][6]=InTrans  #[i][7]=BaulkedLand
          [[0,0],          [.05,35],   [45,2000], [60, 30,.1, 1600,.05,   0,    0,  0  ,    1600],  [0,   0,  0,    0],    [.2],       [0],            [0,  0,    0,0   ]], #AppOLS[0] = non-instrument CN1
          [[0,0],          [.05,55],   [45,2500], [80, 60,.1, 2500,.04,   0,    0 ,   0 ,    2500], [0,   0,  0,    0],    [.2],       [0],            [0,  0,    0,0   ]], #AppOLS[1] = non-instrument CN2
          [[0,0],          [.05,75],   [45,4000], [150,60,.1, 3000,.0333, 0,    0 ,  0  ,    3000], [0,   0,  0,    0],    [.143],     [0],            [0,  0,    0,0   ]], #AppOLS[2] = non-instrument CN3
          [[0,0],          [.05,100],  [45,4000], [150,60,.1, 3000,.025, 0 ,    0 ,  0  ,    3000], [0,   0,  0,    0],    [.143],     [0],            [0,  0,    0,0   ]], #AppOLS[3] = non-instrument CN4
          [[0,0],          [.05,60],   [45,3500], [90, 60,.15,2500,.0333,0 ,    0 ,  0  ,    2500], [0,   0,  0,    0],    [.2],       [0],            [0,  0,    0,0   ]], #AppOLS[4] = INP CN1,2
          [[0,0],          [.05,75],   [45,4000], [150,60,.15,3000,.0333, 3600, .025,8400,15000],   [0,   0,  0,    0],    [.143],     [0],            [0,  0,    0,0   ]], #AppOLS[5] = INP CN3
          [[0,0],          [.05,100],  [45,4000], [300,60,.15,3000,.02,   3600, .025,8400,15000],   [0,   0,  0,    0],    [.143],     [0],            [0,  0,    0,0   ]], #AppOLS[6] = INP CN4
          [[0,0],          [.05,60],   [45,3500], [150,60,.15,3000,.025,  12000,.03 ,0 ,    15000], [90, 60,900,0.025],    [.143],     [.4],           [90, 0,   .1,0.04]], #AppOLS[7] = PA1 CN1,2
          [[150,15000],    [.05,100],  [45,4000], [300,60,.15,3000,.02,   3600, .025,8400,15000],   [120,60,900, 0.02],    [.143],     [.333],         [120,1800,.1,0.033]], #AppOLS[8] = PAI CN3,4
          [[150,15000],    [.05,100],  [45,4000], [300,60,.15,3000,.02,   3600, .025,8400,15000],   [120,60,900, 0.02],    [.143],     [.333],         [120,1800,.1,0.033]], #AppOLS[9] = PAII, III CN3,4
          ]
class TODim:
    #lenght of inner edge = ToOLS[i][0]
    #min dist of inner edge from rwy edge = ToOLS[i][1]
    #Rate of divergence = ToOLS[i][2]
    #final width = ToOLS[i][3]
    #overall length = ToOLS[i][4]
    #slope = ToOLS[i][5]
    ToOLS = [
            [[60] ,[30],[.1  ],[380] ,[1600] ,[.05]],
            [[80] ,[60],[.1  ],[580] ,[2500] ,[.04]],
            [[180],[60],[.125],[1800],[15000],[.02]]
        ]
    TOOLSNAME = [
        ['Take-off'],\
				['Lenght of inner edge',\
                 'Min distance of inner edge from rwy edge',\
                 'Rate of divergence',\
                 'Final width',\
                 'Overall length',\
                 'Slope']
        ]


