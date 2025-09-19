import requests

def get_launches(limit: int = 5):
    base_url = f"https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=30"

    try:
        res = requests.get(base_url)
        res.raise_for_status()
        data = res.json()

        launches = []

        for launch in data.get("results", []):
            launches.append({
                "name" : launch.get("name"),
                "provider" : launch.get("launch_service_provider", {}).get("name"),
                "window_start" : launch.get("window_start"),
                "status" : launch.get("status", {}).get("name"),
                "pad" : launch.get("pad", {}).get("name"),
                "location" : launch.get("pad", {}).get("location", {}).get("name"),
                                                                           
            })
            return {"event" : "launch","launches": launches}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching launch data: {e}")
        return {"event" : "launch","error": str(e)}
    except Exception as e:
        print(f"Error parsing launch data: {e}")
        return {"event" : "launch","error": str(e)}

