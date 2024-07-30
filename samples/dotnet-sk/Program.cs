#pragma warning disable SKEXP0040

using System.Net.Http.Headers;

using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Console;

using dotenv.net;

using Microsoft.SemanticKernel;

using Microsoft.SemanticKernel.ChatCompletion;

using Microsoft.SemanticKernel.Connectors.OpenAI;

using Microsoft.SemanticKernel.Plugins.Core;
using Microsoft.SemanticKernel.Plugins.OpenApi;
using Microsoft.SemanticKernel.Plugins.OpenApi.Extensions;

using Azure.AI.OpenAI;

// Load environment variables
var envVars = DotEnv.Read();
var openAiKey = envVars["AZURE_OPENAI_API_KEY"];
var openAiUrl = envVars["AZURE_OPENAI_ENDPOINT"];
var openAiDeploymentName = envVars["AZURE_OPENAI_DEPLOYMENT_NAME"];

// Kernel builder
var builder = Kernel.CreateBuilder();
builder.Services.AddAzureOpenAIChatCompletion(openAiDeploymentName, openAiUrl, openAiKey);
builder.Services.AddSingleton(new FunctionInvocationFilter());

builder.Services.AddLogging(loggingBuilder =>
{
    loggingBuilder.AddConsole();
    loggingBuilder.SetMinimumLevel(LogLevel.Trace);
});

var kernel = builder.Build();

// Add the plugin, based on the pre-generated OpenAPI plugin spec
var functionParameters = new OpenApiFunctionExecutionParameters();

await kernel.ImportPluginFromOpenApiAsync(
    "PetStoreAPI",
    "../../tests/__fixtures__/llm_friendly_specs/petstore-v3-openapi-plugin.json",
    functionParameters);

// Prepare prompts
var promptTemplateFactory = new KernelPromptTemplateFactory();

var systemPromptTemplate = """
system:
You are a helpful assistant.
Respond to the following prompt by using function calls and then summarize actions.
Ask for clarification if a user request is ambiguous.

user:
{{ $userMessage }}
""";

var promptTemplate = promptTemplateFactory.Create(new PromptTemplateConfig(systemPromptTemplate));

var prompts = new string[] {
    "Find a friendly available savanna pet and display its full details",
};

// Get the chat completion service
var chatCompletionService = kernel.GetRequiredService<IChatCompletionService>();

// Enable auto function calling
OpenAIPromptExecutionSettings openAIPromptExecutionSettings = new()
{
    ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions
};

// Loop through the prompts
foreach (string p in prompts)
{
    var arguments = new KernelArguments
    {
        ["userMessage"] = p,
    };
    var prompt = await promptTemplate.RenderAsync(kernel, arguments);

    ChatHistory history = [];
    history.AddUserMessage(prompt);

    Console.WriteLine("\nQUESTION: " + p);

    // Get the response from the AI
    string result_string = "";
    try
    {
        var result = await chatCompletionService.GetChatMessageContentsAsync(
            history,
            executionSettings: openAIPromptExecutionSettings,
            kernel: kernel);

        // Get the response
        result_string = result[0].ToString();
    }
    catch (Exception e)
    {
        Console.WriteLine("Error: " + e.Message);
    }

    Console.WriteLine("\nANSWER: " + result_string);
}

// Add a function invocation filter to log function invocations
public class FunctionInvocationFilter : IFunctionInvocationFilter
{
    public async Task OnFunctionInvocationAsync(FunctionInvocationContext context, Func<FunctionInvocationContext, Task> next)
    {
        Console.WriteLine("> Function: " + context.Function.Name);
        Console.WriteLine("> (Filter) Arguments: " + string.Join(", ", context.Arguments.Select(a => a.ToString())));

        Console.WriteLine("> (Filter) Modified Arguments: " + string.Join(", ", context.Arguments.Select(a => a.ToString())));

        // await next(context);

        try
        {
            await next(context);
        }
        catch (Exception ex)
        {
            Console.WriteLine("> (Filter) Exception: " + ex.Message);
            throw;
        }
        
        // Console.WriteLine("> Result: " + context.Result);
    }
}
