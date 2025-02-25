
from __future__ import print_function
import time,json
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint
from .models import weather
from datetime import date
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import localtime


def home(request):
    """Render the home page."""

    data=list(weather.objects.values())
    
    return render(request, 'mazao/home.html', {'data':data})
  #  moisture sensor if,or 
def moisture(data):
    daily_will_it_rain = (
        data.get("forecast", {})
        .get("forecastday", [{}])[0]
        .get("day", {})
        .get("daily_will_it_rain", None)
    )

    # Extract humidity and temp_c from current weather data
    humidity = data.get("current", {}).get("humidity", None)
    temp_c = data.get("current", {}).get("temp_c", None)

    print ({
        "daily_will_it_rain": daily_will_it_rain,
        "humidity": humidity,
        "temp_c": temp_c
    })
    model = weather()
    model.cityName = 'Nairobi'
    model.willitraintommorow = daily_will_it_rain
    model.save()

def button_click(request):
    """Handle button click event."""
    if request.method == "POST":


        # Configure API key authorization: ApiKeyAuth
        configuration = weatherapi.Configuration()
        configuration.api_key['key'] = '20cac808bfaf4f99a0782625250602'
        # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
        # configuration.api_key_prefix['key'] = 'Bearer'

        # create an instance of the API class
        api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))
        q = 'nairobi' # str | Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name. Visit [request parameter section](https://www.weatherapi.com/docs/#intro-request) to learn more.
        days = 1 # int | Number of days of weather forecast. Value ranges from 1 to 14
        dt = date.today() # date | Date should be between today and next 14 day in yyyy-MM-dd format. e.g. '2015-01-01' (optional)
        unixdt = dt # int | Please either pass 'dt' or 'unixdt' and not both in same request. unixdt should be between today and next 14 day in Unix format. e.g. 1490227200 (optional)
        hour = 19 # int | Must be in 24 hour. For example 5 pm should be hour=17, 6 am as hour=6 (optional)
        lang = 'eng' # str | Returns 'condition:text' field in API in the desired language.<br /> Visit [request parameter section](https://www.weatherapi.com/docs/#intro-request) to check 'lang-code'. (optional)
        alerts = 'yes' # str | Enable/Disable alerts in forecast API output. Example, alerts=yes or alerts=no. (optional)
        aqi = 'aqi_example' # str | Enable/Disable Air Quality data in forecast API output. Example, aqi=yes or aqi=no. (optional)
        tp = 56 # int | Get 15 min interval or 24 hour average data for Forecast and History API. Available for Enterprise clients only. E.g:- tp=15 (optional)

        try:
            # Forecast API
            api_response = api_instance.forecast_weather(q, days, dt=dt, hour=hour, lang=lang, alerts=alerts)
            print(f'fetched data and is of type {type(api_response)}')
            # pprint(api_response)
            moisture(api_response)
            # pprint(api_response)
        except ApiException as e:
            print("Exception when calling APIsApi->forecast_weather: %s\n" % e)
        return JsonResponse({"message": "Button clicked successfully!"})
    return JsonResponse({"error": "Invalid request"}, status=400)

# api serving data from the software to the microprocessor

def weatherdataapi(request):
    data=list(weather.objects.order_by('-day').values()[:2])
    # weather.objects.order_by('-day')[:2]
    return  JsonResponse(data, safe=False)

@csrf_exempt  
def my_api_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data from request body
            
            # Validate required fields
            required_fields = ["temperature", "humidity", "moisture"]
            if not all(k in data for k in required_fields):
                return JsonResponse({"error": "Missing required fields"}, status=400)
            
            # Extract values
            temperature = data.get("temperature")
            humidity = data.get("humidity")
            moisture = data.get("moisture")

            latestWeather = weather.objects.latest('day')
            willItRain = latestWeather.willitraintommorow
            print(f"will it rain is {willItRain}")

            # Decide irrigation
            if willItRain:
                response_data = {"irrigate": False}
            else:
                response_data = {"irrigate": moisture > 3000}

            return JsonResponse(response_data, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)

