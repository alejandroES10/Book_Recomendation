import asyncio
from dspace_rest_client.client import DSpaceClient

# class DSpaceService:
#     def __init__(self, base_url: str):
#         self.client = DSpaceClient(base_url)

#     async def get_top_community_by_name(self, name: str):
#         top_communities = self.client.get_communities(top=True)
#         print("************Comenzando Proceso de importar tesis*********")
#         for top_community in top_communities:
#             if top_community.name.strip().lower() == name.strip().lower():
#                 return top_community
#         raise ValueError(f"Comunidad '{name}' no encontrada")

#     async def get_items_by_uuid_scope(self, scope_uuid: str, limit=None):
#         items = []
#         cont = 0
#         for item in self.client.search_objects_iter(query="*:*", scope=scope_uuid, dso_type='item'):
#             items.append(item)
#             print(cont)
#             cont += 1
#             if limit and len(items) >= limit:
#                 break
#         return items

#     async def get_bundles_by_item(self, item):
#         return self.client.get_bundles(parent=item)

#     async def get_bitstreams_by_bundle(self, bundle):
#         return self.client.get_bitstreams(bundle=bundle)

#     async def get_items_by_top_community_name(self, community_name: str, limit: int = None):
#         """
#         Devuelve los ítems asociados a una comunidad top específica por su nombre.
#         """
#         try:
#             top_community = await self.get_top_community_by_name(community_name)
#         except ValueError as e:
#             print(f"[ERROR] {e}")
#             return []

#         items = await self.get_items_by_uuid_scope(top_community.uuid, limit)
#         return items


#********    
class DSpaceService:
    def __init__(self, base_url: str):
        self.client = DSpaceClient(base_url)

    async def get_top_community_by_name(self, name: str):
        print("************Comenzando Proceso de importar tesis*********")
        top_communities = await asyncio.wait_for(asyncio.to_thread(self.client.get_communities, top=True),timeout=20)
        for top_community in top_communities:
            if top_community.name.strip().lower() == name.strip().lower():
                return top_community
        raise ValueError(f"Comunidad '{name}' no encontrada")

    async def get_items_by_uuid_scope(self, scope_uuid: str, limit=None):
        def collect_items():
            items = []
            cont = 0
            for item in self.client.search_objects_iter(query="*:*", scope=scope_uuid, dso_type='item'):
                items.append(item)
                cont += 1
                print('Item',cont)
                if limit and len(items) >= limit:
                    break
            return items
        return await asyncio.to_thread(collect_items)

    async def get_bundles_by_item(self, item):
        # return await asyncio.to_thread(self.client.get_bundles, parent=item)
        return await asyncio.wait_for(asyncio.to_thread(self.client.get_bundles, parent=item), timeout=15)

    async def get_bitstreams_by_bundle(self, bundle):
        return await asyncio.to_thread(self.client.get_bitstreams, bundle=bundle)

    async def get_items_by_top_community_name(self, community_name: str, limit: int = None):
        """
        Devuelve los ítems asociados a una comunidad top específica por su nombre.
        """
        try:
            top_community = await self.get_top_community_by_name(community_name)
        except ValueError as e:
            print(f"[ERROR] {e}")
            return []

        return await self.get_items_by_uuid_scope(top_community.uuid, limit)


