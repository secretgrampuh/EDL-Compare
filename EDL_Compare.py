import time
import gspread
from timecode import Timecode
from lxml import etree



exifToolPath = r"C:\Users\zlamplugh\AppData\Roaming\Python\Python37\site-packages\exiftool\exiftool.exe"

def Parse_EDL(EDL_File):
    Shots_List=[]
    Shots_List_withTimecode=[]
    with open(EDL_File,'r') as Before_File:
        Before_Shots=Before_File.read().split("\n")
    clip=None
    timecode=None
    for shot in Before_Shots:
        if "ax" in shot.lower():
            timecode=shot[29:52]
            timecode2=shot[29:]
        if "FROM CLIP NAME:" in shot:
            clip=shot.split("FROM CLIP NAME: ")[1]
            clipCompound=clip+" "+timecode
            clipFullInfo=clip+" "+timecode2
            Shots_List.append(clipCompound)
            Shots_List_withTimecode.append(clipFullInfo)
            clip=None
            timecode=None
    return Shots_List,Shots_List_withTimecode


##### Hard-Coded Inputs
Before_EDL=r"C:\Users\zlamplugh\Desktop\_MMR_ChangeLog\_Actual\EDL\MMRG_CL_v12_GRRM-Notes_FlattenedForEDL_v95.edl"
After_EDL=r"C:\Users\zlamplugh\Desktop\_MMR_ChangeLog\_Actual\EDL\MMRG_CL_v16_flattenedForEDL_v8.edl"
ShotTrack_EDL=r"C:\Users\zlamplugh\Desktop\_MMR_ChangeLog\_Actual\EDL\MMRG_CL_v16_SPJ-Notes_FlattenedEDL_ShotTrack.edl"

xml_file1 = etree.parse(r"C:\Users\zlamplugh\Desktop\_MMR_ChangeLog\_Actual\EDL\ShotGraphics_Only_2.xml")
ShotTrack_Tree=xml_file1.getroot()
Shot_Nodes_List = ShotTrack_Tree.xpath('.//effect/name')
Shot_Names_List=[]
for item in Shot_Nodes_List:
    try:
        if item.text.startswith("MMR_"):
            Shot_Names_List.append(item.text)
    except:
        pass

Before_Shots_List,Before_Shots_List_withTimecode=Parse_EDL(Before_EDL)
After_Shots_List,After_Shots_List_withTimecode=Parse_EDL(After_EDL)
ShotTrack_List,ShotTrack_List_withTimecode=Parse_EDL(ShotTrack_EDL)
ShotTrack_MERGE=[]
i=0
while i<len(ShotTrack_List_withTimecode):
    clip=Shot_Names_List[i]
    ClipTC_Name=ShotTrack_List_withTimecode[i].split(" ")[0]+" "
    clipTC=ShotTrack_List_withTimecode[i].split(ClipTC_Name)[1]
    clipContents=clip+" "+clipTC
    ShotTrack_MERGE.append(clipContents)
    i+=1


After_changes=[]
Before_changes=[]
after_reference=[]
before_reference=[]
for item in After_Shots_List:
    if item not in Before_Shots_List:
        after_reference.append(item)
        FoundItem=False
        for full_item in After_Shots_List_withTimecode:
            if item in full_item:
                FoundItem=True
                After_changes.append(full_item)
        if FoundItem==False:
            After_changes.append(f"Could not find correct key for {item}")

for item in Before_Shots_List:
    if item not in After_Shots_List:
        before_reference.append(item)
        for full_item in Before_Shots_List_withTimecode:
            if item in full_item:
                Before_changes.append(full_item)


with open(r"C:\Users\zlamplugh\Desktop\_MMR_ChangeLog\_Actual\Results.txt",'a') as file:
    print("AfterShotsResults")
    file.write("AfterShotsResults"+"\n")
    for item in After_changes:
        print(item)
        file.write(item+"\n")

    print("\n\n")
    file.write('\n\n')


    print("BeforeShotsResults")
    file.write("BeforeShotsResults"+"\n")

    for item in Before_changes:
        print(item)
        file.write(item+"\n")


    print("\n\n")
    file.write("\n\n")


    print(f"After Changes Len = {len(After_changes)}")
    file.write(f"After Changes Len = {len(After_changes)}+\n")
    print(f"After reference Len = {len(after_reference)}")
    file.write(f"After reference Len = {len(after_reference)}+\n")


    print("\n\n")
    file.write("\n\n")
    print(f"Before Changes Len = {len(Before_changes)}")
    file.write(f"Before Changes Len = {len(Before_changes)}\n")
    print(f"Before reference Len = {len(before_reference)}")
    file.write(f"Before reference Len = {len(before_reference)}\n")



    print('\n\n\n')
    file.write('\n\n\n')

    print("best guesses for after changes")
    file.write("best guesses for after changes\n")

    gc = gspread.service_account()
    sh = gc.open("MMR Redelivery data")
    worksheet = sh.worksheet("Sheet1")

    for item in After_changes:
        results=[]
        clipName=item.split(" ")[0]
        for data in Before_Shots_List_withTimecode:
            if clipName in data:
                results.append(data)
        fileName=item.split(" ")[0]
        timeCodes_RAW=(item.split(fileName+" ")[1])[24:47]
        SHOTNAME_FOR_CHART=""
        for shotline in ShotTrack_MERGE:
            shotName=shotline.split(" ")[0]
            shotline_TCs=(shotline.split(shotName+" ")[1])[24:47]
            if timeCodes_RAW==shotline_TCs:
                SHOTNAME_FOR_CHART=shotName
        timeCodesNewTimeline=(item.split(fileName+" ")[1].replace(" "," , "))
        timelineAppearance=item.split(" ")[3]
        resultString=""
        for piece in results:
            piece2=piece.split(fileName)[1].replace(" "," , ")
            resultString=resultString+piece2+"\n"
        print(f"in new timeline\n{item}\n\nin old timeline\n{results}")
        file.write(f"\n\nIN NEW TIMELINE\n{item}\n\nin old timeline\n{results}\n")
        List_Data=[fileName,timeCodesNewTimeline,resultString,'',SHOTNAME_FOR_CHART,timelineAppearance]
        print(List_Data)
        if len(results)==1:
            tc3=Timecode('23.976', '00:00:00:00')
            newInpoint=Timecode('23.976', (results[0].split(" ")[1]))
            oldInpoint=Timecode('23.976', (timeCodesNewTimeline.split(" , ")[0]))
            newOutpoint=Timecode('23.976', (results[0].split(" ")[2]))
            oldOutPoint=Timecode('23.976', (timeCodesNewTimeline.split(" , ")[1]))
            inpointDifference="00"
            outPointDifference="00"
            message1=""
            message2=""
            if newInpoint!=oldInpoint:
                if newInpoint>oldInpoint:
                    inpointDifference=(newInpoint-oldInpoint)+tc3
                    message1=f"{inpointDifference} added to head"
                elif oldInpoint>newInpoint:
                    inpointDifference=(oldInpoint-newInpoint)+tc3
                    message1=f"{inpointDifference} removed from head"
            if newOutpoint!=oldOutPoint:
                if newOutpoint>oldOutPoint:
                    outPointDifference=(newOutpoint-oldOutPoint)+tc3
                    message2=f"{outPointDifference} removed from tail"
                elif oldOutPoint>newOutpoint:
                    outPointDifference=(oldOutPoint-newOutpoint)+tc3
                    message2=f"{outPointDifference} added to tail"
            if message1=="":
                FrameDifference=message2
            elif message2=="":
                FrameDifference=message1
            else:
                FrameDifference=message1+"\n"+message2
            List_Data=[fileName,timeCodesNewTimeline,resultString,FrameDifference,SHOTNAME_FOR_CHART,timelineAppearance]
        else:
            print(len(results))
        time.sleep(1)
        worksheet.append_row(List_Data)

    print('\n\n\n')
    file.write('\n\n\n')


    print("best guesses for before changes")
    file.write("best guesses for before changes\n")

    for item in Before_changes:
        print("\n")
        file.write('\n')
        inPointDifference=""
        outPointDifference=""
        results=[]
        clipName=item.split(" ")[0]
        for data in After_Shots_List_withTimecode:
            if clipName in data:
                results.append(data)
        fileName=item.split(" ")[0]
        timeCodes_RAW=(item.split(fileName+" ")[1])[24:47]
        SHOTNAME_FOR_CHART=""
        for shotline in ShotTrack_MERGE:
            shotName=shotline.split(" ")[0]
            shotline_TCs=(shotline.split(shotName+" ")[1])[24:47]
            if timeCodes_RAW==shotline_TCs:
                SHOTNAME_FOR_CHART=shotName
        timeCodesOldTimeline=(item.split(fileName+" ")[1]).replace(" "," , ")
        resultString=""
        for piece in results:
            piece2=piece.split(fileName)[1].replace(" "," , ")
            resultString=resultString+piece2+"\n"
        print(f"in old timeline\n{item}\nin new timeline\n{results}")
        file.write(f"IN OLD TIMELINE\n{item}\nin new timeline\n{results}\n")

        timelineAppearance="OLD TIMELINE - "+(item.split(" ")[3])

        List_Data=[fileName,resultString,timeCodesOldTimeline,'',SHOTNAME_FOR_CHART,timelineAppearance]
        if resultString=="":
            timelineAppearance="OLD TIMELINE nowRemoved - "+(timeCodesOldTimeline.split(" , ")[2])
            List_Data=[fileName,resultString,timeCodesOldTimeline,'',SHOTNAME_FOR_CHART,timelineAppearance]
        if len(results)==1:
            tc3=Timecode('23.976', '00:00:00:00')
            newInpoint=Timecode('23.976', (results[0].split(" ")[1]))
            oldInpoint=Timecode('23.976', (timeCodesNewTimeline.split(" , ")[0]))
            newOutpoint=Timecode('23.976', (results[0].split(" ")[2]))
            oldOutPoint=Timecode('23.976', (timeCodesNewTimeline.split(" , ")[1]))
            inpointDifference="00"
            outPointDifference="00"
            message1=""
            message2=""
            if newInpoint!=oldInpoint:
                if newInpoint>oldInpoint:
                    inpointDifference=(newInpoint-oldInpoint)+tc3
                    message1=f"{inpointDifference} added to head"
                elif oldInpoint>newInpoint:
                    inpointDifference=(oldInpoint-newInpoint)+tc3
                    message1=f"{inpointDifference} removed from head"
            if newOutpoint!=oldOutPoint:
                if newOutpoint>oldOutPoint:
                    outPointDifference=(newOutpoint-oldOutPoint)+tc3
                    message2=f"{outPointDifference} removed from tail"
                elif oldOutPoint>newOutpoint:
                    outPointDifference=(oldOutPoint-newOutpoint)+tc3
                    message2=f"{outPointDifference} added to tail"
            if message1=="":
                FrameDifference=message2
            elif message2=="":
                FrameDifference=message1
            else:
                FrameDifference=message1+"\n"+message2
            List_Data=[fileName,resultString,timeCodesNewTimeline,FrameDifference,SHOTNAME_FOR_CHART,timelineAppearance]
        time.sleep(1)
        worksheet.append_row(List_Data)

