import uiautomator2 as u2
import time
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def book_ride(destination, pickup_time):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.gojek.app", stop=False)
        # # accept_permissions(d)
        # # clear_unexpected_popups(d)

        # # # Call login checker
        # # if not check_login_status(d):
        # #     raise Exception("User is not logged in. Please log in to continue.")
        # # clear_unexpected_popups(d)

        # # Continue automation like booking ride
        # # print("📲 Proceeding to book ride...")
        # # d(text="Search for a destination").click()
        # # while not d(resourceId="com.gojek.app:id/2131367370").exists():
        # #     time.sleep(0.1)
        # #     print("waiting for search bar")
        # # d(resourceId="com.gojek.app:id/2131367370").send_keys("airport") # resource id for destination search bar
        # # while not d(resourceId="com.gojek.app:id/2131380508").exists():
        # #     time.sleep(0.1)
        # #     print("waiting for list")
        # # time.sleep(1)
        # # d(resourceId="com.gojek.app:id/2131380508").click() # click first element in the list
        
        # # while not d(resourceId="com.gojek.app:id/2131381640").exists():
        # #     time.sleep(0.1)
        # #     print("waiting for next button")
        # # time.sleep(0.5)
        # # d(resourceId="com.gojek.app:id/2131381640").click() # next on pick up location
        # # # time.sleep(0.5)

        # # while not d(text="Select via map").exists():
        # #     time.sleep(0.1)
        # # time.sleep(0.5)
        # # d(text="Select via map").click() # this element has no id, just use text
        # # # time.sleep(1.5)

        # # while not d(resourceId="com.gojek.app:id/2131381640").exists():
        # #     time.sleep(0.1)
        # #     print("waiting for next button")
        # # time.sleep(0.5)

        # # elNext = find_components(d, "Next")
        # # x1, y1, x2, y2 = map(int, elNext["bounds"].strip("[]").replace("][", ",").split(","))
        # # # Calculate center (x, y)
        # # center_x = (x1 + x2) // 2 
        # # center_y = (y1 + y2) // 2 
        # # d.click(center_x, center_y)
        # # TODO: fetch price list

        # # screen_components(d)
        # # swipe from bottom to top
        # w, h = d.window_size()
        # print(w, h)
        # d.swipe(w * 0.5, h * 0.7, w * 0.5, h * 0.3, 0.3)
        # time.sleep(0.5)
        # comps = find_components_by_id(d, "com.gojek.app:id/text_service_pricing")
        # # comps[i].text is the price with this fomatting "S$5.00", find the cheapest in the comps list, and return the element of the list, not only the price
        # cheapest = min(comps, key=lambda x: float(x["text"].replace("S$", "")))
        # print(coordinate_bounds(cheapest["bounds"]))
        # center_x, center_y = coordinate_bounds(cheapest["bounds"])
        # d.click(center_x, center_y)
        # print(comps)
        # print(cheapest)
        screen_components(d)

        # book car
        comp = find_components_by_id(d, "com.gojek.app:id/tv_title")
        compCoord = coordinate_bounds(comp[0]["bounds"])
        d.click(compCoord[0], compCoord[1])

        time.sleep(0.3)
        # changed price popup
        changed_priced_comp = find_components(d, "There's a change in price")
        if changed_priced_comp is not None:
            book_comp = find_components(d, "book now")
            center_x, center_y = coordinate_bounds(book_comp["bounds"])
            d.click(center_x, center_y)
            
            print("price changed")

    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return