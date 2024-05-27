using Azure.Communication.CallAutomation;
using Azure.Core;
using Microsoft.AspNetCore.Mvc;
using System.Text.Json;
using Azure.Identity;
using Azure;

namespace call_handler.Controllers
{
    [ApiController]
    [Route("call")]
    public class WeatherForecastController : ControllerBase
    {
        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
        }

        [HttpPost]
        public StatusCodeResult Post([FromBody] dynamic request)
        {
            Console.WriteLine("\n\n------------------------------Called Received------------------------------");
            var callbackUrl = "https://incomingcall-python-api.azurewebsites.net/call";
            var callbackUri = new Uri(callbackUrl);
            var endpoint = new Uri("https://voicecallresource.brazil.communication.azure.com/;accesskey=Es26fVjrw3z3vGBQq0lqo4HDlH9QwMqie4mIv2v2VHaKBFzoaXaeM2ljhk68PIqtuB+hl4J2r9GEravehdJGvw==");
            TokenCredential tokenCredential = new DefaultAzureCredential();
            Console.WriteLine(request);
            Console.WriteLine("\n\n\n\n");
            Console.WriteLine(request[0]);
            var callContext = JsonSerializer.Deserialize<Object>(request[0]).data.incomingCallContext;
            var client = new CallAutomationClient(endpoint, tokenCredential);
            Response<AnswerCallResult> result = client.AnswerCall(callContext, callbackUri);
            var callId = result.Value.CallConnection.CallConnectionId;
            CallConnection callConnection = client.GetCallConnection(callId); 
            var audioFileUrl = "https://interactaidata.blob.core.windows.net/test/ns2-st10-sca3-sec12.03.wav";
            var audioFileUri = new Uri(audioFileUrl);
            var audioFile = new FileSource(audioFileUri);
            callConnection.GetCallMedia().PlayToAll(audioFile);
            Console.WriteLine("End call");
            return Ok();
        }
    }
}