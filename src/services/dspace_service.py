import asyncio
from dspace_rest_client.client import DSpaceClient

class DSpaceService:
    def __init__(self, base_url: str):
        self.client = DSpaceClient(base_url)

    async def get_top_community_by_name(self, name: str):
        top_communities = self.client.get_communities(top=True)
        print("***************************Hola")
        for top_community in top_communities:
            if top_community.name.strip().lower() == name.strip().lower():
                return top_community
        raise ValueError(f"Comunidad '{name}' no encontrada")

    async def get_items_by_uuid_scope(self, scope_uuid: str, limit=None):
        items = []
        for item in self.client.search_objects(query="*:*", scope=scope_uuid, dso_type='item'):
            items.append(item)
            if limit and len(items) >= limit:
                break
        return items

    async def get_bundles_by_item(self, item):
        return self.client.get_bundles(parent=item)

    async def get_bitstreams_by_bundle(self, bundle):
        return self.client.get_bitstreams(bundle=bundle)

    async def get_items_by_top_community_name(self, community_name: str, limit: int = None):
        """
        Devuelve los ítems asociados a una comunidad top específica por su nombre.
        """
        try:
            top_community = await self.get_top_community_by_name(community_name)
        except ValueError as e:
            print(f"[ERROR] {e}")
            return []

        items = await self.get_items_by_uuid_scope(top_community.uuid, limit)
        return items
    

async def main():
    dspace_service = DSpaceService(base_url="https://repositorio.cujae.edu.cu//server/api")
    community_top_items = await dspace_service.get_items_by_top_community_name("Tesis de Diploma, Maestrías y Doctorados", limit=10)
    for item in community_top_items:
        print("ITEM METADATA", item.metadata)
        # print(f"Item Handle: {item.handle}, Name: {item.name}, UUID: {item.uuid}")
        bundles = await dspace_service.get_bundles_by_item(item)
        for bundle in bundles:
            print(f"  Bundle Name: {bundle.name}, UUID: {bundle.uuid}")
            bitstreams = await dspace_service.get_bitstreams_by_bundle(bundle)
            for bitstream in bitstreams:
    
                bitstream_uuid = bitstream.uuid 
                url = f"https://repositorio.cujae.edu.cu/server/api/core/bitstreams/{bitstream_uuid}/content"
                print("URL",url)
                print("SIZE", bitstream.sizeBytes)

                # print(f"    Bitstream Name: {bitstream.name}, UUID: {bitstream.uuid}")



if __name__ == "__main__":
    asyncio.run(main())


    

    
