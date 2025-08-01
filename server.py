from flask import Flask, request, jsonify
import subprocess
import hmac, hashlib, time
from pathlib import Path

from Grab.services import book_ride_handler, order_food_handler, confirmation_check_handler
from Grab.services.login import login_otp as grab_login_otp, login as grab_login
from Grab.services.cancel_ride import cancel_ride as grab_cancel_ride
from Grab.services import book_ride_handler, order_food_handler, confirmation_check_handler,  cancel_ride as grab_cancel_ride
from Grab.services.login import login_otp as grab_login_otp, login as grab_login
from Grab.services.food import check_order_food as grab_check_order_food, checkout as grab_checkout
from ryde.service.check_price import check_price as ryde_check_price
from ryde.service.book_ride import book_ride as ryde_book_ride
from ryde.service.cancel_ride import cancel_ride as ryde_cancel_ride
from ryde.service.login import login as ryde_login, login_otp as ryde_login_otp
from foodpanda.check_price import check_price as foodpanda_check_price
from deliveroo.check_price import check_price as deliveroo_check_price
from gojek.check_price import check_price as gojek_check_price
from gojek.book_ride import book_ride as gojek_book_ride
from gojek.cancel_ride import cancel_ride as gojek_cancel_ride
from gojek.login import login as gojek_login
from gojek.login import login_otp as gojek_login_otp
from zig.check_price import check_price as zig_check_price
from zig.cancel_ride import cancel_ride as zig_cancel_ride
from zig.book_ride import book_ride as zig_book_ride
from zig.login import login as zig_login, login_otp as zig_login_otp
from tada.check_price import check_price as tada_check_price
from tada.book_ride import book_ride as tada_book_ride
from tada.cancel_ride import cancel_ride as tada_cancel_ride


from whatsapp.send_message import send_message as whatsapp_send_message
from whatsapp.login import login as whatsapp_login 
import os
import json
import shutil
import time
from data import FlowState, TransportBookingData, parse_booking_options, parse_selected_option, BookingOption, SelectedOption, BookingResult, parse_booking_result, fetch_rides, parse_login_info, FoodOrderData, parse_food_items, parse_order_result, parse_menu_options, MenuOption, OrderResult, MessageData, parse_to, parse_to_options
import time
from dataclasses import asdict

app = Flask(__name__)

@app.route("/health_check", methods=["GET"])
def healthCheck():
    return "API is running", 200
@app.route("/health_check", methods=["GET"])
def health():
    return "API is running", 200

@app.route("/grab", methods=["POST"])
def grab():
    try:
        print("Received request:", request.json)
        print("book_ride is:", book_ride_handler)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        if action == "book_ride":
            booking_option = data.get("booking_option")
            result = book_ride_handler(booking_option)

        elif action == "order_food":
            result = order_food_handler(args.get("item"), args.get("quantity"))

        elif action == "confirmation_check":
            result = confirmation_check_handler(data.get("destination"), data.get("time"))
        # elif action == "cancel_ride":
        #     result = confirmation_check_handler(data.get("destination"), data.get("time"))

        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/gojek", methods=["POST"])
def gojek():
    try:
        print("Received request:", request.json)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        if action == "book_ride":
            ride = data.get("booking_option")
            result = gojek_book_ride(ride)

        # elif action == "order_food":
        #     result = gojek(args.get("item"), args.get("quantity"))

        elif action == "confirmation_check":
            result = gojek_check_price(data.get("destination"), data.get("time"))
        elif action == "cancel_ride":
            result = gojek_cancel_ride()

        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/zig", methods=["POST"])
def zig():
    try:
        print("Received request:", request.json)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        if action == "book_ride":
            booking_option = data.get("booking_option")
            result = zig_book_ride(booking_option)

        # elif action == "order_food":
        #     result = gojek(args.get("item"), args.get("quantity"))

        elif action == "confirmation_check":
            result = zig_check_price(data.get("destination"), data.get("time"))
        elif action == "cancel_ride":
            result = zig_cancel_ride(data.get("destination"), data.get("time"))

        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/ryde", methods=["POST"])
def ryde():
    try:
        print("Received request:", request.json)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        if action == "book_ride":
            booking_option = data.get("booking_option")
            result = ryde_book_ride(booking_option)

        # elif action == "order_food":
        #     result = gojek(args.get("item"), args.get("quantity"))

        if action == "confirmation_check":
            result = ryde_check_price(data.get("destination"), data.get("time"))
        # elif action == "cancel_ride":
        #     result = zig_cancel_ride(data.get("destination"), data.get("time"))

        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/foodpanda", methods=["POST"])
def foodpanda():
    try:
        print("Received request:", request.json)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        # if action == "order_food":
        #     booking_option = data.get("booking_option")
        #     result = ryde_book_ride(booking_option)

        if action == "confirmation_check":
            print(data)
            result = foodpanda_check_price(data.get("restaurant"), data.get("dropoff"), data.get("order"))
        # elif action == "cancel_ride":
        #     result = zig_cancel_ride(data.get("destination"), data.get("time"))

        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/all_transport_app", methods=["POST"])
def all_transport_app():
    try:
        time_start = time.time()
        print("Received request:", request.json)
        print("book_ride is:", book_ride_handler)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        result = []
        if action == "confirmation_check":
            ryde_result = ryde_check_price(data.get("destination"), data.get("time"))
            grab_result = confirmation_check_handler(data.get("destination"), data.get("time"))
            gojek_result = gojek_check_price(data.get("destination"), data.get("time"))
            zig_result = zig_check_price(data.get("destination"), data.get("time"))
            result = {
                "grab": grab_result,
                "gojek": gojek_result,
                "zig": zig_result,
                "ryde": ryde_result
            }
        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)
        end_time = time.time()
        print(f"Execution time: {end_time - time_start:.4f} seconds")
        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/transport/flow", methods=["POST"])
def transport_flow():
    req = request.get_json()

    flow = req.get("flow")
    step = req.get("step")
    raw_data = req.get("data", {})
    print("step:", step, "raw data:", raw_data)
    data = TransportBookingData(
        pickup_location=raw_data.get("pickup_location", ""),
        destination=raw_data.get("destination", ""),
        time=raw_data.get("time", "now"),
        app=raw_data.get("app"),
        login_info=parse_login_info(raw_data.get("login_info")),
        is_payment_default_exist=raw_data.get("is_payment_default_exist", True),
        confirmation_check_done=raw_data.get("confirmation_check_done", False),
        booking_options=parse_booking_options(raw_data.get("booking_options", [])),
        selected_option=parse_selected_option(raw_data.get("selected_option")),
        booking_result=parse_booking_result(raw_data.get("booking_result")),
        cancelled=raw_data.get("cancelled", False)
    )

    state = FlowState(flow="transport_booking", step=step, data=data)

    # FSM Logic
    if state.step == "start":
        state.step = "awaiting_missing_info"

    elif state.step == "awaiting_missing_info":
        if state.data.destination:
            state.step = "confirmation_check_pending"
    elif state.step == "login":
        print("login step")
        # login action
        if state.data.app.lower() == "gojek":
            res = gojek_login(state.data.login_info.phone_number)
            if res["status"] == "success":
                print("waiting otp")
        elif state.data.app.lower() == "grab":
            res = grab_login(state.data.login_info.phone_number)
            if res["status"] == "success":
                print("waiting otp")
        # elif state.data.app.lower() == "tada":
        #     res = tada_login(state.data.login_info.phone_number)
        #     if res["status"] == "success":
        #         print("waiting otp")
        elif state.data.app.lower() == "ryde":
            res = ryde_login(state.data.login_info.phone_number)
            if res["status"] == "success":
                print("waiting otp")
        elif state.data.app.lower() == "zig":
            res = zig_login(state.data.login_info.phone_number)
            if res["status"] == "success":
                print("waiting otp")
        state.step = "login_otp_pending"
    
    elif state.step == "login_otp_pending":
        print("otp:", state.data.login_info.otp)
        if state.data.app.lower() == "gojek":
            res = gojek_login_otp(state.data.login_info.otp)
            if res["status"] == "success":
                print("login success")
        elif state.data.app.lower() == "grab":
            res = grab_login_otp(state.data.login_info.otp)
            if res["status"] == "success":
                print("login success")
        # elif state.data.app.lower() == "tada":
        #     res = tada_login_otp(state.data.login_info.otp)
        #     if res["status"] == "success":
        #         print("login success")
        elif state.data.app.lower() == "ryde":
            res = ryde_login_otp(state.data.login_info.otp)
            if res["status"] == "success":
                print("login success")
        elif state.data.app.lower() == "zig":
            res = zig_login_otp(state.data.login_info.otp)
            if res["status"] == "success":
                print("login success")
        state.data.is_logged_in = True
        state.step = "confirmation_check_pending"
    elif state.step == "confirmation_check_pending":
        booking_options = []
        
        if state.data.app is None:
            tada_result = tada_check_price(state.data.destination, state.data.time)
            if tada_result is not None:
                if not (isinstance(tada_result, dict) and tada_result["status"] == "not_logged_in"):
                    for i, opt in enumerate(tada_result):
                        booking_options.append(
                        BookingOption(
                            title=opt["title"],
                            app="tada",
                            price=opt["price"],
                            option_id=f"{opt['title'].lower().replace(' ', '')}-tada-{i:03}"
                        )
                    )
                    
            ryde_result = ryde_check_price(state.data.destination, state.data.time)
            if ryde_result is not None:
                if not (isinstance(ryde_result, dict) and ryde_result["status"] == "not_logged_in"):
                    for i, opt in enumerate(ryde_result):
                        booking_options.append(
                        BookingOption(
                            title=opt["title"],
                            app="ryde",
                            price=opt["price"],
                            option_id=f"{opt['title'].lower().replace(' ', '')}-ryde-{i:03}"
                        )
                    )
            grab_result = confirmation_check_handler(state.data.destination, state.data.time)
            if grab_result is not None:
                if not (isinstance(grab_result, dict) and grab_result["status"] == "not_logged_in"):
                    for i, opt in enumerate(grab_result):
                        booking_options.append(
                            BookingOption(
                                title=opt["title"],
                                app="grab",
                                price=opt["price"],
                                option_id=f"{opt['title'].lower().replace(' ', '')}-grab-{i:03}"
                            )
                        )
            gojek_result = gojek_check_price(state.data.destination, state.data.time)
            if gojek_result is not None:
                if not (isinstance(gojek_result, dict) and gojek_result["status"] == "not_logged_in"):
                    for i, opt in enumerate(gojek_result):
                        booking_options.append(
                        BookingOption(
                            title=opt["title"],
                            app="gojek",
                            price=opt["price"],
                            option_id=f"{opt['title'].lower().replace(' ', '')}-gojek-{i:03}"
                        )
                    )
            zig_result = zig_check_price(state.data.destination, state.data.time)
            if zig_result is not None :
                if not (isinstance(zig_result, dict) and zig_result["status"] == "not_logged_in"):
                    for i, opt in enumerate(zig_result):
                        booking_options.append(
                        BookingOption(
                            title=opt["title"],
                            app="zig",
                            price=opt["price"],
                            option_id=f"{opt['title'].lower().replace(' ', '')}-zig-{i:03}"
                        )
                    )
        elif (state.data.app.lower() == "grab"):
            grab_result = confirmation_check_handler(state.data.destination, state.data.time)
            if grab_result is not None:
                if not (isinstance(grab_result, dict) and grab_result["status"] == "not_logged_in"):
                    for i, opt in enumerate(grab_result):
                        booking_options.append(
                            BookingOption(
                                title=opt["title"],
                                app="grab",
                                price=opt["price"],
                                option_id=f"{opt['title'].lower().replace(' ', '')}-grab-{i:03}"
                            )
                        )
                else:
                    state.data.is_logged_in = False
                    state.step = "login"
                    return jsonify(asdict(state))

        elif (state.data.app.lower() == "ryde"):
            ryde_result = ryde_check_price(state.data.destination, state.data.time)
            if ryde_result is not None:
                if not (isinstance(ryde_result, dict) and ryde_result["status"] == "not_logged_in"):
                    for i, opt in enumerate(ryde_result):
                        booking_options.append(
                        BookingOption(
                            title=opt["title"],
                            app="ryde",
                            price=opt["price"],
                            option_id=f"{opt['title'].lower().replace(' ', '')}-ryde-{i:03}"
                        )
                    )
                else:
                    state.data.is_logged_in = False
                    state.step = "login"
                    return jsonify(asdict(state))
        elif state.data.app.lower() == "gojek":
            gojek_result = gojek_check_price(state.data.destination, state.data.time)
            if gojek_result is not None:
                if not (isinstance(gojek_result, dict) and gojek_result["status"] == "not_logged_in"):
                    for i, opt in enumerate(gojek_result):
                        booking_options.append(
                        BookingOption(
                            title=opt["title"],
                            app="gojek",
                            price=opt["price"],
                            option_id=f"{opt['title'].lower().replace(' ', '')}-gojek-{i:03}"
                        )
                    )
                else:
                    state.data.is_logged_in = False
                    state.step = "login"
                    return jsonify(asdict(state))

        elif state.data.app.lower() == "tada":
            tada_result = tada_check_price(state.data.destination, state.data.time)
            if tada_result is not None:
                if not (isinstance(tada_result, dict) and tada_result["status"] == "not_logged_in"):
                    for i, opt in enumerate(tada_result):
                        booking_options.append(
                        BookingOption(
                            title=opt["title"],
                            app="tada",
                            price=opt["price"],
                            option_id=f"{opt['title'].lower().replace(' ', '')}-tada-{i:03}"
                        )
                    )
                else:
                    state.data.is_logged_in = False
                    state.step = "login"
                    return jsonify(asdict(state))
        elif state.data.app.lower() == "zig":
            zig_result = zig_check_price(state.data.destination, state.data.time)
            if zig_result is not None:
                if not (isinstance(zig_result, dict) and zig_result["status"] == "not_logged_in"):
                    for i, opt in enumerate(zig_result):
                        booking_options.append(
                        BookingOption(
                            title=opt["title"],
                            app="zig",
                            price=opt["price"],
                            option_id=f"{opt['title'].lower().replace(' ', '')}-zig-{i:03}"
                        )
                    )
                else:
                    state.data.is_logged_in = False
                    state.step = "login"
                    return jsonify(asdict(state))
        state.data.booking_options = booking_options
        state.data.confirmation_check_done = True
        state.step = "awaiting_user_confirmation"

    elif state.step == "awaiting_user_confirmation":
        if state.data.selected_option:
                state.step = "booking_in_progress"


    elif state.step == "booking_in_progress":
        res = None
        if state.data.app.lower() == "grab":
            res = book_ride_handler(state.data.selected_option.title) 
        elif state.data.app.lower() == "ryde":
            res = ryde_book_ride(state.data.selected_option.title)
        elif state.data.app.lower() == "gojek":
            res = gojek_book_ride(state.data.selected_option.title)
        elif state.data.app.lower() == "zig":
            res = zig_book_ride(state.data.selected_option.title)
        elif state.data.app.lower() == "tada":
            res = tada_book_ride(state.data.selected_option.title)
        if res["status"] == "no_payment_default":
            state.data.is_payment_default_exist = False
            state.step = "confirmation_check_pending"
            return jsonify(asdict(state))
        state.data.booking_result = BookingResult(status=res["status"], waiting_time=res["waiting_time"])
        state.step = "handle_waiting_time"

    elif state.step == "handle_waiting_time":
        if state.data.booking_result and state.data.booking_result.waiting_time > 10:
            state.step = "cancel_and_restart"
        else:
            state.step = "done"

    elif state.step == "cancel_and_restart":
        if state.data.app.lower() == "grab":
            grab_cancel_ride()
        elif state.data.app.lower() == "ryde":
            ryde_cancel_ride()
        elif state.data.app.lower() == "gojek":
            gojek_cancel_ride()
        elif state.data.app.lower() == "tada":
            tada_cancel_ride()
        elif state.data.app.lower() == "zig":
            zig_cancel_ride()
        state.data.selected_option = None
        state.data.booking_result = None
        state.data.confirmation_check_done = False
        state.step = "confirmation_check_pending"

    return jsonify(asdict(state))

@app.route("/food/flow", methods=["POST"])
def food_flow():
    req = request.get_json()

    flow = req.get("flow")
    step = req.get("step")
    raw_data = req.get("data", {})
    print("step:", step, "raw data:", raw_data)

    data = FoodOrderData(
        delivery_location=raw_data.get("delivery_location", ""),
        restaurant_name=raw_data.get("restaurant_name", ""),
        food_items=parse_food_items(raw_data.get("food_items", [])),
        app=raw_data.get("app"),
        login_info=parse_login_info(raw_data.get("login_info")),
        is_payment_default_exist=raw_data.get("is_payment_default_exist", True),
        confirmation_check_done=raw_data.get("confirmation_check_done", False),
        menu_options=parse_menu_options(raw_data.get("menu_options", [])),
        selected_option=parse_selected_option(raw_data.get("selected_option")),
        order_result=parse_order_result(raw_data.get("order_result")),
        cancelled=raw_data.get("cancelled", False)
    )

    state = FlowState(flow="food_ordering", step=step, data=data)

    if state.step == "start":
        state.step = "awaiting_missing_info"

    elif state.step == "awaiting_missing_info":
        print("state.data.delivery_location:", state.data.delivery_location, "state.data.restaurant_name:", state.data.restaurant_name, "state.data.food_items:", state.data.food_items)
        if state.data.delivery_location and state.data.restaurant_name and state.data.food_items:
            state.step = "confirmation_check_pending"
            print("update step to confirmation_check_pending")

    elif state.step == "login":
        # res = login_to_app(state.data.app, state.data.login_info.phone_number)
        res = {"status": "success"}
        if res["status"] == "success":
            state.step = "login_otp_pending"

    elif state.step == "login_otp_pending":
        # res = verify_otp(state.data.app, state.data.login_info.otp)
        res = {"status": "success"}
        if res["status"] == "success":
            state.data.is_logged_in = True
            state.step = "confirmation_check_pending"

    elif state.step == "confirmation_check_pending":
        # options = get_menu_options(
        #     app=state.data.app,
        #     restaurant=state.data.restaurant_name,
        #     food_items=state.data.food_items
        # )
        options = []

        orders = [
            {
                "name": order.name,
                "pcs": order.quantity,
                "pref": "regular",
            }
            for order in state.data.food_items
        ]
        print("orders:", orders)
        if state.data.app is None:
            grab_res = grab_check_order_food(state.data.restaurant_name, state.data.delivery_location, orders, state.data.delivery_note)
            if grab_res is not None:
                if not (isinstance(grab_res, dict) and grab_res["status"] == "not_logged_in"):
                    options.append(grab_res)

            foodpanda_res = foodpanda_check_price(state.data.restaurant_name, state.data.delivery_location, orders, state.data.delivery_note)
            if foodpanda_res is not None:
                print("cek logic", not (isinstance(foodpanda_res, dict) and foodpanda_res["status"] == "not_logged_in"))
                if not (isinstance(foodpanda_res, dict) and foodpanda_res["status"] == "not_logged_in"):
                    print("response:", foodpanda_res)
                    options.append(foodpanda_res)

            deliveroo_res = deliveroo_check_price(state.data.restaurant_name, state.data.delivery_location, orders)
            if deliveroo_res is not None:
                if not (isinstance(deliveroo_res, dict) and deliveroo_res["status"] == "not_logged_in"):
                    options.append(deliveroo_res)
            # options = [
            #     {
            #         "app": "grab",
            #         "price": "$20"}
            #         ,
            #     {
            #         "app": "foodpanda",
            #         "price": "$20"},
            #         {
            #         "app": "deliveroo",
            #         "price": "$20"},
                
            # ]
        print("options:", options)
        if isinstance(options, list):
            state.data.menu_options = [
                MenuOption(
                    app=opt["app"],
                    price=opt["price"],
                    option_id=f"{opt["app"]}-{i:03}",
                    orders=state.data.food_items
                )
                for i, opt in enumerate(options)
            ]
            state.data.confirmation_check_done = True
            state.step = "awaiting_user_confirmation"
        elif options.get("status") == "not_logged_in":
            state.data.is_logged_in = False
            state.step = "login"
            return jsonify(asdict(state))

    elif state.step == "awaiting_user_confirmation":
        if state.data.app:
            state.step = "ordering_in_progress"

    elif state.step == "ordering_in_progress":
        # res = place_order(state.data.app, state.data.selected_option.title)
        # if res["status"] == "no_payment_default":
        #     state.data.is_payment_default_exist = False
        #     state.step = "confirmation_check_pending"
        #     return jsonify(asdict(state))
        res = {"status": "success", "estimated_delivery_time": 20}
        state.data.order_result = OrderResult(status=res["status"], estimated_delivery_time=res["estimated_delivery_time"])
        state.step = "handle_estimated_time"

    elif state.step == "handle_estimated_time":
        
            state.step = "done"

    elif state.step == "cancel_and_restart":
        # cancel_order(state.data.app)
        state.data.selected_option = None
        state.data.order_result = None
        state.data.confirmation_check_done = False
        state.step = "confirmation_check_pending"

    print("sent state: ", state)
    return jsonify(asdict(state))


@app.route("/messaging/flow", methods=["POST"])
def message_flow():
    req = request.get_json()

    step = req.get("step")
    print("step:", step, "raw data:", req)

    data = MessageData(
        step=req.get("step", ""),
        app=req.get("app", ""),
        to=parse_to(req.get("to", [])),
        to_options=parse_to_options(req.get("to_options", [])),
        message=req.get("message", ""),
        image=req.get("image", ""),
        login_qr=req.get("login_qr", "")
    )

    if step == "login":
        data.login_qr = ""
        # if res["status"] == "choose_contact":
        #     data.to_options = res["contact"]
        #     data.to = ""
    # elif step == "wait_for_qr":

    elif step == "send_message":
        res = whatsapp_send_message(data.to, data.message)
        # res = {"status": "not_logged_in", "login_qr": "https://c206abf8b79ee2544bf4d5d0e9e1b8e6.r2.cloudflarestorage.com/heypico-note/recordings/1752657308315_qr.jpeg"}
        # res = {"message": "contact list", "status": "choose_contact", "contact": [{"to": "john", "options": ["john doe", "john smith", "john smith jr"]}, {"to": "jane", "options": ["jane doe", "jane smith", "jane smith jr"]}] }
        # res = {"message": "message sent", "status": "success"}
        print("res:", res)
        if res["status"] == "not_logged_in":
            data.login_qr = res["login_qr"]
        elif res["status"] == "choose_contact":
            data.to_options = res["contact"]
            # data.to = 
    elif step == "choose_contact":
        data.to_options = None
        res = whatsapp_send_message(data.to, data.message)
        # res = {"message": "message sent", "status": "success"}

        # print("res:", res)
    print("data:", data)
    return jsonify(asdict(data))
import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,  # or DEBUG, WARNING, etc.
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("server.log"),  # writes to a file
        logging.StreamHandler()             # also prints to console
    ]
)
@app.route('/stop-tunnel', methods=['POST'])
def stop_tunnel():
    data = request.get_json()
    screen_name = "tunnel"

    try:
        # --- Stop Cloudflare Tunnel ---
        if shutil.which("screen"):
            try:
                screen_list = subprocess.check_output(["screen", "-ls"], text=True, stderr=subprocess.STDOUT)
                if f"\t{screen_name}\t" in screen_list or f".{screen_name}\t" in screen_list:
                    subprocess.run(["screen", "-S", screen_name, "-X", "quit"], check=False)
                    print(f"Stopped screen session: {screen_name}")
                else:
                    print("Screen running, but session not found. Fallback to pkill cloudflared.")
                    subprocess.run(["pkill", "-f", "cloudflared"], check=False)
            except subprocess.CalledProcessError:
                print("No screen session exists. Fallback to pkill cloudflared.")
                subprocess.run(["pkill", "-f", "cloudflared"], check=False)
        else:
            print("screen command not found. Falling back to pkill cloudflared.")
            subprocess.run(["pkill", "-f", "cloudflared"], check=False)

        # --- Remove health-check cron job ---
        cron_line = "/data/data/com.termux/files/home/.termux/boot/health-check-cron.sh"
        try:
            current_cron = subprocess.check_output(["crontab", "-l"], text=True)
            new_cron = "\n".join(
                line for line in current_cron.splitlines()
                if cron_line not in line
            )
            subprocess.run(["crontab", "-"], input=new_cron, text=True, check=True)
            print("Cron job removed.")
        except subprocess.CalledProcessError:
            print("No crontab set yet — skipping removal.")

        # --- Remove secret folder ---
        secret_path = os.path.expanduser("~/.secret")
        if os.path.exists(secret_path) and os.path.isdir(secret_path):
            shutil.rmtree(secret_path)
            print("~/.secret folder removed.")

        return jsonify({
            "message": f"Tunnel stopped and cron removed (if any)."
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update', methods=['POST'])
def stop_tunnel():
    try:
        boot_dir = os.path.expanduser("~/.termux/boot")
        health_script_path = os.path.join(boot_dir, "update-script.sh")
        subprocess.Popen(["bash", health_script_path])

        return jsonify({
            "message": f"Tunnel stopped and cron removed (if any)."
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/register-tunnel', methods=['POST'])
def trigger_tunnel():
    data = request.get_json()
    tunnel_name = data.get('name')
    user_id = data.get('userId')
    secret = data.get('secret')

    logging.info(f"Received tunnel registration request: {data}")

    if not tunnel_name:
        return jsonify({'error': 'Missing tunnel name'}), 400
    if not user_id:
        return jsonify({'error': 'Missing user id'}), 400
    if not secret:
        return jsonify({'error': 'Missing secret'}), 400

    try:
        process = subprocess.Popen(
            ["bash", "./start-tunnel.sh", tunnel_name, user_id, secret],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        boot_dir = os.path.expanduser("~/.termux/boot")
        health_script_path = os.path.join(boot_dir, "health-check.sh")
        cron_script_path = os.path.join(boot_dir, "health-check-cron.sh")
 
        base_url = f"https://{tunnel_name}.heypico1.xyz"
        subprocess.run([
            "sed", "-i", f"s|^BASE_URL=.*|BASE_URL=\\\"{base_url}\\\"|", health_script_path
        ])

        subprocess.Popen(["bash", cron_script_path])

        return jsonify({
            "message": f"Tunnel '{tunnel_name}' is launching in background.",
            "pid": process.pid,
            "tunnel_name": tunnel_name,
            "user_id": user_id,
            "secret": secret
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
      
def verify_hmac(request):
    received_signature = request.headers.get("X-Signature")
    logging.info(f"Received tunnel stop sign: {received_signature}")

    if not received_signature:
        return False
    SHARED_SECRET = ""
    secret_path = Path.home() / ".secret" / "secret.key"
    if secret_path.exists():
        with open(secret_path, "rb") as f:
            SHARED_SECRET = f.read().strip()
    else:
        print(f"[WARN] Secret file not found at {secret_path}, using default key.")
        SHARED_SECRET = b"secret"
    # Construct the message (you can customize this)
    message = request.get_data()  # Raw body content
    logging.info(f"Received tunnel stop request: {message}")

    # Generate HMAC using secret
    expected_signature = hmac.new(SHARED_SECRET, message, hashlib.sha256).hexdigest()

    return hmac.compare_digest(received_signature, expected_signature)


@app.before_request
def hmac_auth_middleware():
    excluded_routes = ['healthCheck','trigger_tunnel']  # Name of the view function
    if request.endpoint in excluded_routes:
        return 
    if not verify_hmac(request):
            return jsonify({"error": "Unauthorized", "message": "Invalid Token"}), 403

# test auth endpoint
@app.route("/indextest", methods=["POST"])
def indextest():
    return "API is running", 200
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)