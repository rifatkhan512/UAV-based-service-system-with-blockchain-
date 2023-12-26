from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
from django.views.decorators.csrf import csrf_exempt

hash_digest = [
'be95d38117b0a5ce796419f812ee82ae50adcb8bcc037b6a6f070af024544f92',
'7e518c8398d75f90803c3c170a7f26e920928aceeba949aabd2ede20bf25006e',
'e216659660c4bddc2359dcf9821744648e27400b5de358d6097552623523742f',
'79285bc97619a39f7b992eac760d32725a2bbea4f5c0738d322ffa4740124d31',
'fd678411202feed2cd22a1e96ef8af3ea0dcd5d5faa621be9e5102bb4dd99876',
'd5bf89ef7f1d70247de8293d6d271cf1e28057b825b0e3b936e2104702b62f22',
'9e4f3b854b2c1cfc7bf8e71b944e42170b6d71e1fa847e1c00e004e0e0017389',
'8ef03af6cc1b889df7b81bcfab24ece8423b7d3eda378ace7d76ab58abdb5855',
'6c301faf8b96e4fe7ce3a9ef91c02980e86bfc5fafc9d53ed78b3e400d5b298c',
'17da1a86da4cf98571a5228e3cc87afdd81fb2831e0d7fb62cea81e985b136a0',
'9f4fc401fddcd2961dcafa74d513d43c07415d102d08b3c274ce8b7ba7d7ce7d',
'63813911bf9eee4612fb52c5e611ba3ed9501b53594df90d822f613c6f12aa96',
'681becbb48f6bae7b742cc1d190cf8aa611f50b289cb77832c674bfc9d6cb82c',
'506770e22b479ec106575c8d7e68cb28b8a56ec600dd9bdc96188d5ac2b21e57',
'469b3fef11387af1182599c5b76131c2757e15dac993b7e744d3db8300204819',
'698cc28875bd91189c43c175a1a48ab16e82c7954a2bc21dcd315a3b1a683314',
'c694441c134f51466cbebe05ca58946a0a43decea3734562e6f6652ef8027ada',
'f9f2c90a40785389116f9a967f2f92bdcb358d3fe06f0a703844add058aae039',
'3eb32f8af6e16e9e533975786988c11a7c11d1df7eeadff348479e2de0e544f6',
'0e9a5abcd757bc8d6ad966fd5b2db102b410d8cc1adde2c7e9d48987cb911867',
]


#@api_view(['GET'])

def ApiOverview(request):
	api_urls = {
		'all_items': '/',
		'Search by name': '/?name=category_name',
		'Add': '/create',
		'Update': '/update/pk',
		'Delete': '/item/pk/delete'
		
	}

	return Response(api_urls)


@api_view(['POST'])

def add_items(request):
	item = ItemSerializer(data=request.data)
	items=Item.objects.all()
	# validating for already existing data
	if Item.objects.filter(**request.data).exists():
		raise serializers.ValidationError('This data already exists')
	if item.is_valid():
		item.save()
		print(item.data)
		n= len(ItemSerializer(items, many=True).data)
		j=n-1+len(hash_digest)
		j%=len(hash_digest)
		print("previous hash: {}".format(hash_digest[j]))
		j+=1
		j%=len(hash_digest)
		print("current hash: {}".format(hash_digest[j]))
		print(f"saved {n} times")
		return Response(item.data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_items(request):
	# checking for the parameters from the URL
	if request.query_params:
		items = Item.objects.filter(**request.query_params.dict())
	else:
		items = Item.objects.all()

	# if there is something in items else raise error
	if items:
		serializer = ItemSerializer(items, many=True)
		return Response(serializer.data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_items(request, pk):
	item = Item.objects.get(pk=pk)
	data = ItemSerializer(instance=item, data=request.data)

	if data.is_valid():
		data.save()
		print(data.data)
		return Response(data.data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@csrf_exempt
def delete_items(request, pk):
	item = get_object_or_404(Item, pk=pk)
	item.delete()
	return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def get_item_by_id(request, pk):
	if request.query_params:
		items = Item.objects.filter(**request.query_params.dict())
	else:
		items = Item.objects.all()

	# if there is something in items else raise error
	if items:
		serializer = ItemSerializer(items, many=True)
		if (pk<=0) or (pk>len(serializer.data)):
			return Response(status=status.HTTP_404_NOT_FOUND)
		return Response(serializer.data[pk-1])
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['DELETE'])
@csrf_exempt
def delete_all(request):
	items = Item.objects.all().delete()

	""" serializer = ItemSerializer(items, many=True)
	l=len(serializer.data)
	for i in range(1,l+1):
			item = get_object_or_404(Item,pk=l)
			item.delete() """
	return Response(status=status.HTTP_202_ACCEPTED)
        
        
