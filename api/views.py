from rest_framework.views import APIView
from rest_framework.response import Response

from .models import StoreGPSData
from .models import StoreCornerCordsData
from .models import StoreNodeData

import sys
sys.path.append("..")
from scripts import coordinateMath

class GPSView(APIView):
    def get(self, request, format=None):
        gpsDict = {}

        try:
            gpsObjects = StoreGPSData.objects.all()
    
            for gpsItem in gpsObjects:
                gpsDict[gpsItem.name] = gpsItem.gpsCord

            return Response(gpsDict, status=200)
        except:
            return Response(status=404)

    def post(self, request, format=None):
        gpsItems = request.data['gps']
        bad_gpsItems = []

        for gpsItem in gpsItems:
            try:
                new_gpsItem = StoreGPSData(name=gpsItem['name'], gpsCord=gpsItem['gpsCord'])
                new_gpsItem.save()
            except:
                bad_gpsItems.append(gpsItem)
        
        if len(bad_gpsItems) > 0:
            return Response({"INVALID GPS DATA": bad_gpsItems}, status=200)
        else:
            return Response(status=200)

class CornerCordsView(APIView):
    def get(self, request, format=None):
        gpsCornerCordItems = request.query_params['buildingName']

        try:
            gpsCornerCordObjects = None
            try:
                gpsCornerCordObjects = StoreCornerCordsData.objects.get(buildingName=gpsCornerCordItems)
            except:
                return Response({}, status=200)

            return Response({"buildingName": gpsCornerCordObjects.buildingName, "cords": gpsCornerCordObjects.cornerCords}, status=200)
        except:
            return Response(status=404)

    def post(self, request, format=None):
        gpsCornerCordItems = request.data['gpsCornerCord']
        bad_gpsCornerCordItems = []

        existingItems = StoreCornerCordsData.objects.all().filter(buildingName=gpsCornerCordItems[0]['buildingName'])
        if len(existingItems) == 0:
            for gpsCornerCordItem in gpsCornerCordItems:
                try:
                    new_gpsCornerCordItem = StoreCornerCordsData(buildingName=gpsCornerCordItem['buildingName'], cornerCords=gpsCornerCordItem['cornerCords'])
                    new_gpsCornerCordItem.save()
                except:
                    bad_gpsCornerCordItems.append(gpsCornerCordItem)
        else:
            gpsCornerCordObjects = existingItems[0]
            gpsCornerCordObjects.cornerCords = gpsCornerCordItems[0]['cords']['cornerCords']
            gpsCornerCordObjects.save()

        if len(bad_gpsCornerCordItems) > 0:
            return Response({"INVALID GPS CORNER CORD DATA": bad_gpsCornerCordItems}, status=200)
        else:
            return Response(status=200)


class NodeView(APIView):
    def get(self, request, format=None):
        nodeBuildingName = request.query_params['buildingName']
        nodeFloorName = request.query_params['floorName']

        try:
            nodeObjects = StoreNodeData.objects.all().filter(buildingName=nodeBuildingName)
            if len(nodeObjects) == 0:
                 return Response({}, status=200)

            return Response(nodeObjects[0].nodes, status=200)
        except:
            return Response(status=404)

    def post(self, request, format=None):
        nodeItem = request.data['node']
        bad_nodeItems = []

        fourCornerItems = StoreCornerCordsData.objects.all().filter(buildingName=nodeItem['buildingName'], floorName=nodeItem['floorName'])
        print("OKASOAKSOKASO")
        # coordinateMath.findGPSCoordinates(gpsArr, gesturePos, listOfGestures) - returns list of gps locations corresponding to listOfGestures (same order)
        coordinateMath.main()
        try:
            new_nodeItem = StoreNodeData(buildingName=nodeItem['buildingName'], floorName=nodeItem['floorName'], nodes=nodeItem['nodes'])
            new_nodeItem.save()
        except:
            bad_nodeItems.append(nodeItem)
        
        if len(bad_nodeItems) > 0:
            return Response({"INVALID NODE DATA": bad_nodeItems}, status=200)
        else:
            return Response(status=200)