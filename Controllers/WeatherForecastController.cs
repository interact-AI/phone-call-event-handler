using Azure.Communication.CallAutomation;
using Microsoft.AspNetCore.Mvc;
using Azure;
using Newtonsoft.Json;


namespace call_handler.Controllers
{
    class ResponseWrapperWrapper
    {
        public string incomingCallContext { get; set; }

        public static ResponseWrapperWrapper FromJson(string json) => JsonConvert.DeserializeObject<ResponseWrapperWrapper>(json);

    }
    class ResponseWrapper
    {
        public ResponseWrapperWrapper data { get; set; }

        public static ResponseWrapper FromJson(string json) => JsonConvert.DeserializeObject<ResponseWrapper>(json);    
    }   
    [ApiController]
    [Route("call")]
    public class WeatherForecastController : ControllerBase
    {
        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
        }

        [HttpPost]
        public async Task<StatusCodeResult> Post([FromBody] dynamic request)
        {
            Console.WriteLine("\n\n------------------------------Called Received------------------------------");
            var callbackUrl = "https://incomingcall-python-api.azurewebsites.net/call";
            var callbackUri = new Uri(callbackUrl);
            var endpoint = ("endpoint=https://voicecallresource.brazil.communication.azure.com/;accesskey=Es26fVjrw3z3vGBQq0lqo4HDlH9QwMqie4mIv2v2VHaKBFzoaXaeM2ljhk68PIqtuB+hl4J2r9GEravehdJGvw==");
            string requestString = request[0].ToString();
            ResponseWrapper callContextJson = ResponseWrapper.FromJson(requestString);
            var callContext = callContextJson.data.incomingCallContext;
            var client = new CallAutomationClient(endpoint);
            Response<AnswerCallResult> result = client.AnswerCall(callContext, callbackUri);
            var callId = result.Value.CallConnection.CallConnectionId;
            CallConnection callConnection = client.GetCallConnection(callId); 
            var audioFileUrl = "https://interactaidata.blob.core.windows.net/test/ns2-st10-sca3-sec12.03.wav";
            var audioFileUri = new Uri(audioFileUrl);
            var audioFile = new FileSource(audioFileUri);
            Console.WriteLine("Esperando 2 segundos a conexion...");
            await Task.Delay(2000);
            Console.WriteLine("Va el audio");
            callConnection.GetCallMedia().PlayToAll(audioFile);
            Console.WriteLine("End call");
            return Ok();
        }
    }
}