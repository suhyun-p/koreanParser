from konlpy.tag import Kkma
kkma = Kkma()

class attrDic:
    keywordList = []
    attrList = []

    def __init__(self):
        self.keywordList.append('냄새/NNG')
        self.attrList.append(['나/NP'])
        self.keywordList.append('가격/NNG')
        self.attrList.append(['착하/VA'])
        self.keywordList.append('배송/NNG')
        self.attrList.append(['빠르/VA'])

    def getAttrList(self, keyword):
        if keyword in self.keywordList:
            i = self.keywordList.index(keyword)
            if i > -1:
                return self.attrList[i]



class chnkDetail:
    chnkList = [] # ['가격/NNG', '대비/NNG', '최고/NNG', '에/JKM', '요/JX']
    text = ''
    sToken = ''  # 가격/NNG
    sTag = '' # NNG
    eToken = ''  # 요/JX
    eTag = ''  # JX
    eToken_1 = 'None' # 에/JKM
    eTag_1 = 'None' # JKM
    length = 0;
    i = 0
    def __init__(self, chnkList):
        if len(chnkList) > 0:
            if type(chnkList[0]) is str: # ['가격/NNG', '대비/NNG', '최고/NNG', '에/JKM', '요/JX']
                self.chnkList = chnkList # ['가격/NNG', '대비/NNG', '최고/NNG', '에/JKM', '요/JX']
                self.text = str(chnkList)
                self.length = len(chnkList)
                self.sTag = chnkList[0].split('/')[1] # NNG
                self.eTag = chnkList[-1].split('/')[1] # JX
                self.sToken = chnkList[0] # 가격/NNG
                self.eToken = chnkList[-1] # 요/JX
                if len(chnkList) > 1:
                    self.eToken_1 = chnkList[-2] # 에/JKM
                    self.eTag_1 = chnkList[-2].split('/')[1] # JKM
            elif type(chnkList[0]) is chnkDetail: # [ chnkDetail(['화질/NNG', '도/JX']), chnkDetail(['좋/VA', '고/ECE']) ... ]
                for i in range(len(chnkList)):
                    self.chnkList.append(chnkList[i].chnkList)
                    self.text += chnkList[i].text
                    self.length += chnkList[i].length
                self.text = '[' + self.text + ']'
                self.sTag = chnkList[0].sTag
                self.eTag = chnkList[-1].eTag
                self.sToken = chnkList[0].sToken
                self.eToken = chnkList[-1].sToken

class ruleDetail:
    r1SCheck = False
    r1ECheck = False
    r2SCheck = False
    r2ECheck = False
    r3SCheck = False
    r3ECheck = False
    r1SList = []
    r1EList = []
    r2SList = []
    r2EList = []
    r3SList = []
    r3EList = []
    ruleDepth = 0
    def __init__(self, rule):
        if len(rule[0][0]) > 0: self.r1SCheck = True
        if len(rule[0][1]) > 0: self.r1ECheck = True
        if len(rule[1][0]) > 0: self.r2SCheck = True
        if len(rule[1][0]) > 0: self.r2ECheck = True
        if len(rule[2][0]) > 0: self.r3SCheck = True
        if len(rule[2][0]) > 0: self.r3ECheck = True

        self.r1SList = rule[0][0]
        self.r1EList = rule[0][1]
        self.r2SList = rule[1][0]
        self.r2EList = rule[1][1]
        self.r3SList = rule[2][0]
        self.r3EList = rule[2][1]

        if self.r3SCheck or self.r3ECheck: self.ruleDepth = 3
        elif self.r2SCheck or self.r2ECheck: self.ruleDepth = 2
        elif self.r1SCheck or self.r1ECheck: self.ruleDepth = 1

class ruleCheckResult:
    applyYN = False
    context = []
    packaged= []
    def __init__(self, applyYn, context, packaged):
        self.context = context
        self.packaged = packaged
        self.applyYN = applyYn

class tokenPackage:
    tokenList = [] # '화질/NNG', '도/JX', '좋/VA', '고/ECE' ...
    length = 0;
    i = 0;

    def __init__(self, tokenList):
        self.tokenList = tokenList # '화질/NNG', '도/JX', '좋/VA', '고/ECE' ...
        self.length = len(tokenList)

    def index(self, i):
        self.i = i
        return self.tokenList[i]

    def nextTag(self):
        if self.i < self.length - 1:
            return self.tokenList[self.i + 1].split('/')[1]
        else:
            return 'None'

    def nextToken(self):
        if self.i < self.length - 1:
            return self.tokenList[self.i + 1]
        else:
            return 'None'

class chnkPackage:
    chnkList = []  # chnkDetail(['화질/NNG', '도/JX']), chnkDetail(['좋/VA', '고/ECE']) ...
    length = 0;
    i = 0;

    def __init__(self, chnkList):
        self.chnkList = chnkList  # chnkDetail(['화질/NNG', '도/JX']), chnkDetail(['좋/VA', '고/ECE']) ...
        self.length = len(chnkList)

    def index(self, i):
        self.i = i
        return self.chnkList[i]

    def next(self):
        if self.i < self.length - 1:
            return self.chnkList[self.i+1]
        else:
            return 'None'

    def next2(self):
        if self.i < self.length - 2:
            return self.chnkList[self.i+2]
        else:
            return 'None'

    def nextTag(self):
        if self.i < self.length - 1:
            return self.chnkList[self.i + 1].split('/')[1]
        else:
            return 'None'

    def nextToken(self):
        if self.i < self.length - 1:
            return self.chnkList[self.i + 1]
        else:
            return 'None'

class textAnalyzer:
    text = ""
    tokenized = []
    tagList = []
    eList = ['EPH', 'EPT', 'EPP', 'EFN', 'EFQ', 'EFO', 'EFA', 'EFI', 'EFR', 'ECE', 'ECS', 'ECD', 'ETN', 'ETD']  # 어미
    jList = ['JKS', 'JKC', 'JKG', 'JKO', 'JKM', 'JKI', 'JKQ', 'JC', 'JX']  # 관계언
    vList = ['VV', 'VA', 'VXV', 'VXA', 'VCP', 'VCN']  # 용언
    sList = ['SF', 'SE', 'SS', 'SP', 'SO', 'SW']
    exceptList = ['MAG', 'MAC']

    def __init__(self, text):
        self.text = text
        self.tokenized = self.tokenize() # '화질/NNG', '도/JX', '좋/VA', '고/ECE' ...
        self.tagList = self.setTagList() # NNG, JX, VA, ECE ...
        self.chnkListDep1 = self.setChnkDep1() # ['화질/NNG', '도/JX']['좋/VA', '고/ECE'] ...
        self.chnkPackage = self.setChnkPackage() # [ chnkDetail(['화질/NNG', '도/JX']), chnkDetail(['좋/VA', '고/ECE']) ... ]
        self.contextList = self.setContextList()
        self.chnkListDep2 = self.setChnkDep2()

    def tokenize(self):
        return ['/'.join(t) for t in kkma.pos(self.text)]

    def setTagList(self):
        tagList = []
        for i in range(len(self.tokenized)):
            tagList.append(self.tokenized[i].split('/')[1])
        return tagList

    def setChnkDep1(self): # '화질/NNG', '도/JX' >> ['화질/NNG', '도/JX'] '좋/VA', '고/ECE' >> ['좋/VA', '고/ECE']
        ret = []
        t_ret = []
        tokenList = tokenPackage(self.tokenized)
        for i in range(len(self.tokenized)):
            token = tokenList.index(i)
            tag = token.split('/')[1]
            nextTag = tokenList.nextTag()

            if tag in self.sList or tag == 'EMO':  # 기호 및 Emoticon 제외
                continue

            t_ret.append(token)
            if nextTag in self.exceptList or nextTag in self.vList:  # MAG나 용언(동사, 형용사) 앞에서 나눔
                if len(t_ret) > 0:
                    ret.append(t_ret)
                t_ret = []
            if tag in self.eList or tag in self.jList:  # 어미나 관계언(조사)에서 나눔
                if nextTag in self.eList or nextTag in self.jList:  # 다음 토큰도 어미나 관계언이면 Pass
                    pass
                else:
                    if len(t_ret) > 0:
                        ret.append(t_ret)
                    t_ret = []
            if tag in self.exceptList:  # MAG나 기호에서 나눔
                if len(t_ret) > 0:
                    ret.append(t_ret)
                t_ret = []

            if token == '배송/NNG' and nextTag  == 'NNG':
                if len(t_ret) > 0:
                    ret.append(t_ret)
                t_ret = []

        if len(t_ret) > 0:
            ret.append(t_ret)
        t_ret = []
        return ret

    def setChnkPackage(self):
        ret = []
        for i in range(len(self.chnkListDep1)):
            ret.append(chnkDetail(self.chnkListDep1[i]))
        return chnkPackage(ret)

    def setContextList(self):
        t_ret = []
        ret = []

        eList = self.eList[:] # eList와 self.eList가 동일한 참조를 가져 슬라이싱([:]) 추가
        if 'ETD' in eList:
            eList.pop(eList.index('ETD')) # ['있/VV', '는/ETD']['브랜드/NNG', '에/JKM']

        detailList = self.chnkPackage
        for i in range(detailList.length): # chnkDetail(['화질/NNG', '도/JX']), chnkDetail(['좋/VA', '고/ECE']) ...
            detail = detailList.index(i)
            nextDetail = detailList.next()
            t_ret.append(detail)

            if detail.eTag in eList: # 기본적으로, 어미로 끝나면 줄나눔
                #if nextDetail != 'None' and nextDetail.sTag in eList:
                    # pass
                if nextDetail != 'None' and ( nextDetail.sTag == 'VXV' or nextDetail.sTag == 'VXA') :
                    # 어미 + 보조동사는 줄나눔 X : 하/XSV 고/ECE 있/VXV 었/EPT ...
                    # 어미 + 보조형용사는 줄나눔 X : ['권하/VV', '고/ECE'] ['싶/VXA', '은/ETD']
                    pass
                else:
                    if len(t_ret) > 0:
                        ret.append(t_ret)
                    t_ret = []

            if detail.eToken == '요/JX': # ~에요(에/JKM, 요/JX)로 끝나면 줄나눔
                if detail.eToken_1 == '에/JKM':
                    if len(t_ret) > 0:
                        ret.append(t_ret)
                    t_ret = []

            if detail.eToken == '하지만/MAC': # ['콩알/NNG', '만/JX']['하지만/MAC']['과일/NNG', '맛/NNG', '이/JKS']
                if len(t_ret) > 0:
                    ret.append(t_ret)
                t_ret = []

        if len(t_ret) > 0:
            ret.append(t_ret)
        t_ret = []
        return ret

    def printContextList(self):
        for i in range(len(self.contextList)):
            temp_string = ''
            for j in range(len(self.contextList[i])):
                temp_string += self.contextList[i][j].text
            print(temp_string)
            #self.printDecorized(chnkSetLv2(self.packageList[i]))
            #self.printDecorized(self.contextList[i])
        print('')

    def ruleCheck(self, rDetail, context):
        index = -1
        ret = []
        t_ret = []
        for i in range(len(context)):
            r1SPass = False
            r1EPass = False
            r2SPass = False
            r2EPass = False
            r3SPass = False
            r3EPass = False

            detail = context[i]
            nextDetail = 'None'
            nextDetail1 = 'None'
            if i < len(context) - 1:
                nextDetail = context[i + 1]
            if i < len(context) - 2:
                nextDetail1 = context[i + 2]

            if rDetail.ruleDepth == 1:
                if rDetail.r1SCheck:
                    if detail.sTag in rDetail.r1SList: r1SPass = True
                if rDetail.r1ECheck:
                    if detail.eTag in rDetail.r1EList: r1EPass = True

                if r1SPass or r1EPass:
                    index = i
                    break

            if rDetail.ruleDepth == 2:
                if rDetail.r1SCheck:
                    if detail.sTag in rDetail.r1SList: r1SPass = True
                if rDetail.r1ECheck:
                    if detail.eTag in rDetail.r1EList: r1EPass = True

                if r1SPass or r1EPass:
                    if rDetail.r2SCheck:
                        if nextDetail != 'None' and nextDetail.sTag in rDetail.r2SList: r2SPass = True
                    if rDetail.r2ECheck:
                        if nextDetail != 'None' and nextDetail.eTag in rDetail.r2EList: r2EPass = True

                    if r2SPass or r2EPass:
                        index = i
                        break

            if rDetail.ruleDepth == 3:
                if rDetail.r1SCheck:
                    if detail.sTag in rDetail.r1SList: r1SPass = True
                if rDetail.r1ECheck:
                    if detail.eTag in rDetail.r1EList: r1EPass = True

                if r1SPass or r1EPass:
                    if rDetail.r2SCheck:
                        if nextDetail != 'None' and nextDetail.sTag in rDetail.r2SList: r2SPass = True
                    if rDetail.r2ECheck:
                        if nextDetail != 'None' and nextDetail.eTag in rDetail.r2EList: r2EPass = True

                    if r2SPass or r2EPass:
                        if rDetail.r3SCheck:
                            if nextDetail1 != 'None' and nextDetail1.sTag in rDetail.r3SList: r3SPass = True
                        if rDetail.r3ECheck:
                            if nextDetail1 != 'None' and nextDetail1.eTag in rDetail.r3EList: r3EPass = True

                        if r3SPass or r3EPass:
                            index = i
                            break

        if index != -1:
            t_flag = False
            t_count = rDetail.ruleDepth
            t_list = []
            for i in range(index, index+t_count):
                t_list.append(i)

            for i in range(len(context)):
                if i in t_list:
                    t_flag = True
                    t_ret.append(context[i])
                else:
                    if t_flag == True:
                        t_flag = False
                        ret.append(chnkDetail(t_ret))
                        t_ret = []
                        ret.append(context[i])
                    else:
                        ret.append(context[i])
            if len(t_ret) > 0:
                ret.append(chnkDetail(t_ret))
                t_ret = []
            return ruleCheckResult(True, context, ret)
        else:
            ret = context
            return ruleCheckResult(False, context, ret)

    def setChnkDep2Element(self, context): # [ chnkDetail(), chnkDetail(), ... ]
        ret = []
        t_ret = []

        ruleList = []

        # ['좋/VA', '은/ETD']['것/NNB']['같/VA', '아요/EFN']
        # ['하/VV', 'ㄹ/ETD']['수/NNB']['있/VV', '어서/ECD']]
        # ['믿/VV', '을/ETD']['수/NNB']['있/VV', '는/ETD']
        rule1 = [
            [
                []
                , ['ETD']
            ]
            , [
                ['NNB']
                ,['NNB']
            ]
            , [
                ['VA', 'VV', 'VCN']
                ,[]
            ]
        ]

        # ['권하/VV', '고/ECE']['싶/VXA', '은/ETD']
        # ['챙기/VV', '어/ECS']['주/VXV', '고/ECE']
        # ['하/VV', '어/ECS']['주/VXV', '시/EPH', '고/ECE']
        # ['나쁘/VA', '지/ECD']['않/VXV', '고/ECE']
        rule2 = [
            [
                []
                , ['ECE', 'ECS', 'ECD']
            ]
            , [
                ['VXA', 'VXV']
                , []
            ]
            , [
                []
                , []
            ]
        ]

        ruleList.append(rule1)
        ruleList.append(rule2)

        ruleCheckResultList = []
        for i in range(len(ruleList)):
            rDetail = ruleDetail(ruleList[i])
            ruleCheckResultList.append(self.ruleCheck(rDetail, context))

        appliedCount = 0
        appliedResult = ruleCheckResult(False, context, context)
        for i in range(len(ruleCheckResultList)):
            if ruleCheckResultList[i].applyYN:
                appliedCount += 1
                appliedResult = ruleCheckResultList[i]

        if appliedCount > 1:
            print('********** applied duplicated **********')

        return appliedResult.packaged

        '''
        for i in range(len(context)):
            detail = context[i]
            nextDetail = 'None'
            nextDetail1 = 'None'
            if i < len(context)-1:
                nextDetail = context[i+1]
            if i < len(context)-2:
                nextDetail = context[i+2]
        '''
        '''
        if nextDetail != 'None' and nextDetail.sTag == 'NNB':
            if detail.eTag == 'ETD':
                if nextDetail1 != 'None' and (nextDetail1.sTag == 'VA' or nextDetail1.sTag == 'VV'):
                    ret.append(detail)
                    ret.append(nextDetail)
                    ret.append(nextDetail1)
                    i += 2
                    continue
        else:
            ret.append(detail)
        '''
        '''
            if detail.eTag == 'ETD':
                if len(t_ret) > 0 and t_ret[-1].eTag == 'NNB':  # ETD > NNB
                    if printYN: print('t_ret add16 : ', detail.text)
                    t_ret.append(detail)
                    ret.append(chnkDetail(t_ret))
                else:
                    if printYN: print('t_ret add19 : ', detail.text)
                    t_ret.append(detail)

                #if printYN: print('t_ret add1 : ', detail.text)
                #t_ret.append(detail)
            elif detail.sTag == 'NNB':
                if len(t_ret) > 0 and t_ret[-1].eTag == 'ETD': # ETD > NNB
                    if printYN: print('t_ret add2 : ', detail.text)
                    t_ret.append(detail)
                else:
                    if len(t_ret) > 0:
                        for i in range(len(t_ret)):
                            if printYN: print('ret add3 : ', t_ret[i].text)
                            ret.append(t_ret[i])
                        t_ret = []
                        if printYN: print('ret add4 : ', detail.text)
                        ret.append(detail)
                    else:
                        if printYN: print('ret add5 : ', detail.text)
                        ret.append(detail)
            elif detail.sTag == 'VA' or detail.sTag == 'VV':
                if len(t_ret) > 0 and t_ret[-1].eTag == 'NNB': # ETD > NNB > VA/VV
                    if printYN: print('t_ret add6 : ', detail.text)
                    t_ret.append(detail)
                    ret.append(chnkDetail(t_ret))
                else:
                    if len(t_ret) > 0:
                        for i in range(len(t_ret)):
                            if printYN: print('ret add7 : ', t_ret[i].text)
                            ret.append(t_ret[i])
                        t_ret = []
                        if printYN: print('ret add8 : ', detail.text)
                        ret.append(detail)
                    else:
                        if printYN: print('ret add9 : ', detail.text)
                        ret.append(detail)
            else:
                if len(t_ret) > 0:
                    for i in range(len(t_ret)):
                        if printYN: print('ret add10 : ', t_ret[i].text)
                        ret.append(t_ret[i])
                    t_ret = []
                    if printYN: print('ret add11 : ', detail.text)
                    ret.append(detail)
                else:
                    if printYN: print('ret add12 : ', detail.text)
                    ret.append(detail)
'''
        #return ret

    def setChnkDep2(self):
        ret = []
        for i in range(len(self.contextList)):
            ret.append(self.setChnkDep2Element(self.contextList[i]))

        return chnkPackage(ret) # class

    def printChnkListDep2(self):
        for i in range(len(self.chnkListDep2.chnkList)):
            temp_string = ''
            for j in range(len(self.chnkListDep2.chnkList[i])):
                #print(self.chnkListDep2.chnkList[i][j].text)
                temp_string += self.chnkListDep2.chnkList[i][j].text
            print(temp_string)
            self.printDecorized(self.chnkListDep2.chnkList[i])
        print('')

    def printDecorized(self, chnkListDep2):  # chnkSetLv2(['화질/NNG', '도/JX']), chnkDetail(['좋/VA', '고/ECE']...)
        for i in range(len(chnkListDep2)):
            detail = chnkListDep2[i]
            nextDetail = 'None'
            beforeDetail = 'None'
            if i < len(chnkListDep2)-1:
                nextDetail = chnkListDep2[i+1]
            if i > 0:
                beforeDetail = chnkListDep2[i-1]

            # ['착하/VA', 'ㄴ/ETD'] > ['가격/NNG', '에다/JC']
            if detail.eTag == 'ETD':
                if nextDetail != 'None' and nextDetail.sTag == 'NNG':
                    print('\t', detail.text, '>', nextDetail.text)

            # ['배송/NNG']['많이/MAG']['느리/VA', 'ㅂ니다/EFN']
            if detail.sTag == 'MAG':
                if nextDetail != 'none' and (nextDetail.sTag == 'VA' or nextDetail.sTag == 'VV' or nextDetail.sTag == 'NNG' or nextDetail.sTag == 'XR' or nextDetail.sTag == 'NP'):
                    print('\t', detail.text, '>', nextDetail.text)
                    if beforeDetail != 'None' and beforeDetail.eTag == 'NNG':
                        print('\t', beforeDetail.text, '<', nextDetail.text)

            # ['화질/NNG', '도/JX'] < ['좋/VA', '고/ECE']
            if detail.sTag == 'NNG':
                if nextDetail != 'None' and (nextDetail.sTag == 'VA' or nextDetail.sTag == 'VV'):
                    print('\t', detail.text, '<', nextDetail.text)




        '''
        if detail.sTag == 'NNG':
            if nextDetail != 'None' and nextDetail.sTag != 'MAG':
                if nextDetail.sTag == 'VA' or nextDetail.sTag == 'VV':  # ['배송/NNG']['빠르/VA', '고/ECE']['가격/NNG']['싸/VV', '고/ECE']
                    print('\t', detail.chnkList, '<', nextDetail.chnkList)
            elif nextDetail != 'None' and nextDetail.sTag == 'MAG':
                if nextDetail2 != 'None' and (nextDetail2.sTag == 'VA' or nextDetail2.sTag == 'VV'): # ['목/NNG']['안/MAG']['늘어나/VV', '었/EPT', '으면/ECD']
                    print('\t', detail.chnkList, '<', nextDetail.chnkList, '<', nextDetail2.chnkList)

        if detail.sTag == 'NNB':
            if nextDetail != 'None' and nextDetail.sTag != 'MAG':
                if nextDetail.sTag == 'VA' or nextDetail.sTag == 'VV':  # ['거/NNB']['같/VA', '아요/EFN']
                    print('\t', detail.chnkList, '<', nextDetail.chnkList)

        if detail.eTag == 'ETD':
            if nextDetail != 'None' and nextDetail.sTag == 'NNG': # ['착하/VA', 'ㄴ/ETD']['가격/NNG', '에다/JC']
                print('\t', detail.chnkList, '>', nextDetail.chnkList)
            if nextDetail != 'None' and nextDetail.sTag == 'NNB': # ['좋/VA', '은/ETD']['것/NNB']
                print('\t', detail.chnkList, nextDetail.chnkList)

        # ['나쁘/VA', '지/ECD']['않/VXV', '고/ECE']
        # ['챙기/VV', '어/ECS']['주/VXV', '고/ECE']
        if detail.eTag == 'ECD' or detail.eTag == 'ECS':
            if nextDetail != 'None' and (nextDetail.sTag == 'VXV' or nextDetail.sTag == 'VXA'):
                print('\t', detail.chnkList, nextDetail.chnkList)

        '''
        '''
        if nextDetail != 'None' and (nextDetail.sTag == 'VA' or nextDetail.sTag == 'VV'):
            # ['화질/NNG', '도/JX']['좋/VA', '고/ECE']
            # ['가격/NNG']['싸/VV', '고/ECE']
            if detail.sTag == 'NNG': # ['가격/NNG', '에다/JC'] < ['빠르/VA', 'ㄴ/ETD']
                if detail.eTag == 'JC' or detail.eTag == 'JKM':
                    # ['가격/NNG', '에다/JC']['빠르/VA', 'ㄴ/ETD']
                    # ['배송/NNG', '에/JKM'] < ['정해지/VV', 'ㄴ/ETD']
                    # ['배송/NNG', '맘/NNG', '에/JKM']['드/VV', 'ㅁ니다/EFN'] --> Conflict
                    pass
                else:
                    print('\t', detail.chnkList, '<', nextDetail.chnkList)
        '''


textList = []
textList.append('냄새가좀나서 받자마자 세탁했는데.. 목안늘어났으면 좋겠네용ㅠㅠ')
textList.append('착한 가격에다 빠른배송 맘에듬니다 연근 조림할때 넣었더니 윤기가 좌르르하니맛있네요')
textList.append('홈플러스 간단히 장보기 조은거 같아요ㆍ배송조 빠르구요ㆍ 부산오데ㅣㅇ 양도 좋고 가격도 착하고 맛도 괜찬은거같아요ㆍ')
textList.append('빠르고 친절한 배송에 정해진 시간에 오니까 너무 편리하네요  가격도 시중가에 비해 훨씬 저렴하네요')
textList.append('들깨가루를 구입을 하였는데 가격도 좋고 빠른 배송으로 빠르게 구입을 할수 있어서 너무 좋았습니다 다른 사람에게도 권하고 싶은 제품입니다 감사합니다')
textList.append('주위분들이 비타민이 좋다하여 부모님과 제가 먹으려고 2개 구입했습니다. 추석명절전이라 추석전에 도착할까 걱정 많이했는데 다행히 도착하여 부모님께 잘 선물해 드렸습니다. 빠른 배송 감사드리며, 몇번을 포장하여 안전하게 도착했습니다. 비타민 잘 먹고 부모님과 제가 올 겨울에는 감기 걱정없이 보냈으면 합니다.')
textList.append('딸기맛 사탕 구입하다가 이걸로 바꿨는데. 가격도 나쁘지 않고. 크기는 콩알만 하지만 과일맛이 여러가지라서 좋네요. 어차피 향이랑 색소 차이라서 녹으면 설탕 맛입니다. 배송 많이 느립니다. 한시간 넘게 느려요.')
textList.append('배송빠르고 가격싸고 사은품챙겨주고 무엇보다 믿을수있는 브랜드에 업체가 확실하여 주져없이 주문했어요  최~~~고!!!!')
textList.append('사이즈 넉넉하지 않고')
textList.append('사이즈 넉넉하지 아니하고')
textList.append('사이즈 넉넉하고 프린트도 예뻐서 마음에 들어요 동생도 보더니 예쁘다고 자기꺼도 사달래네요 배송도 빠르고 만족합니다 많이 파세요!')
textList.append('아직 안 써봐서 뭐 할 수는 없지만  일단 배송 빨랐어요 이번엔 꼭 임신 됐으면 좋겠네요^^ 다른분들도 이쁜아기 낳고 행복하세요^^')
textList.append('아직 안 써봐서 뭐리 할 수는 없지만  일단 배송 빨랐어요 이번엔 꼭 임신 됐으면 좋겠네요^^ 다른분들도 이쁜아기 낳고 행복하세요^^')
textList.append('배송 정말 하루만에 오네요 천천히 와도 되는데.. 맛은 초코가 좀더 맛있는겨 같아요 그래도 잘 먹을게요')
textList.append('초기불량으로 교환요청했는데 보낼생각을 안하다가 글 남기니까 배송하네요 ㅋㅋㅋ')
textList.append('아이가 태어나서 부터 먹던 제품 이렇게 포장부터 다른 안전 배송은 처음이네요.  좋아요. 굿')
textList.append('화질도 좋고, 소리도 잘 들리고 가격대비 최고에요! 추석 연휴라서 배송 안 될꺼라 생각하고 있었는데  대체휴일에도 배송 해 주시고... 덕분에 애들이 너무 좋아하네요! 진심 감사합니다~^^ 번창하세요??')
textList.append('추석연휴에 주문하는 바람에 연휴끝나고도 한참후에 받을줄 알았더니.. 까만날돌아오자마자 총알배송! 1600짜리 이렇게 싼것도 없는데 정말 잘샀어요!')
textList.append('여기서 두번사먹어봐서 가격이저렴하게올라왔길래 믿고샀습니다. 근데..고추양념만너무많이들어있고 갓김치포기는몇개안되네요..차라리 이렇게파실거면 싸게팔지말고 원래파시던가격으로파세요~~ 배송은맘에들었으나 상품은별로네요;;; 재구매는 좀생각해봐야할것같네요.')
textList.append('배송은 빠르네요 발도편하고 부담없이 신기 좋아요 근데... 앞에 리본이 삐뚤해요~ 신을때마다 잘 정리하고 신어야겠어요')
textList.append('새집으로 이사와서 새집증후군이 생기는듯하여 주문했어요~ 배송이 어떻게 올지 궁금했는데 엄청 잘싸져서 왔네요. 감사합니다. 잘키울게요~ 이 아이는 하루하루 다르게 크네요.')
textList.append('브릿츠 스피커 작은거 쓰다가 이번에 새로나온 제품 구매했네요 라디오도 나와서 쉽게 들을 수 있을 거 같네요 배송도 엄청 빨리와서 더더욱 좋아요')
textList.append('배송빨라서 좋았습니다. 기존와이파이가 고장나서 구매하게 되었는데 속도, 인식률등등 다방면적으로마음에 드네요~~ 문의가있어 전화드렸더니 친절하게 응대해주셔서 기분좋았습니다~^^')
textList.append('좋은 선물이 되었어요  명절연휴 끝나고 또 추가주문했는데 금액이 좀 오른거죠? 그래도 먹기에도 선물로도 고급지고 맘에 들어요 좋아요 좋아요 롯데**에서 7만원대에 팔더군요 70미리 60개~')
textList.append('아버지 생신 선물로 사드렸는데 이쁘네요.')
textList.append('가격도 매우 저렴하고 일단 맛이 입맛에 당길 정도로 칼칼하고 부드러워요 맛있어요 배송도 빠르고 친절합니다')
textList.append('가격도매우저렴히고일단맛이입맛에당길정도로칼칼하고브두워요 맛있어요 배송도빠르고친절합니다')
textList.append('재작년에 에넥스에서 보트 사서 아주 만족스럽게 사용하고 있는데 이번에 튜브두개 또 샀네요...튜브 마무리나 두께가 확실히 두껍고 안전해 보여서 좋네요... ')
textList.append('인터넷 이미지 보다 훨씬 더 크고 튼튼하네요 색상도 밝은 아이보리 색상으로 훨씬 이쁘네요 배송도 빠르고 배송기사님도 친철합니다. 적극 추천합니다.')
textList.append('터래기가 자알 안 까끼요.  또 문제는 같은 모델인데도 상표가 제각각..  여튼 전에 삿던 카이저가 괜찮아 상표 보고 선물용으로 20개 구매했는데 주고 욕 먹는거 아닌지..')

for i in range(len(textList)):
    tokenSet = textAnalyzer(textList[i])
    #print(tokenSet.tokenized)
    #print(tokenSet.tagList)
    #print(tokenSet.chnkListDep1)
    #tokenSet.printContextList()
    tokenSet.printChnkListDep2()


#a = attrDic()
print(attrDic().getAttrList('배송/NNG'))