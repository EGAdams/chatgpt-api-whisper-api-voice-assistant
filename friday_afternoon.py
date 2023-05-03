Before we start refactoring the code, it is advisable that we define responsibilities for the new classes that will be formed from this view controller.

According to the Single Responsibility Principle (SRP) in SOLID design principles, each class should have only one reason to change. For example, the new classes should be responsible for handling each of the following:
- Handling user interactions with web view
- Parsing requests and handling them
- Registering and handling push notifications
- Logging

Now let's get started with the refactoring. Please note that the rewritten code is broken down into several classes.

First, let's create a new file 'JavascriptInterface.swift' and add the following code:

```swift
class JavascriptInterface: NSObject, WKScriptMessageHandler {

    typealias McbaReadyCallback = () -> ()
    
    var mcbaReady = false
    var webView: WKWebView!
    var mmcbaReadyCallback: McbaReadyCallback?
 
    let scheme = "mcba-ios"
    
    init( view: WKWebView ) {
        webView = view
        super.init()
    }
    
    func bind() {
        let cmd = "var Device = { " +
            "setTemplateRoot: function(root) { }, " +
            "onPageLoaded: function(page) { window.location = 'mcba-ios:onPageLoaded/' + page; }, " +
            "onScriptLoaded: function(src) { }, " +
            "showToast: function(msg) { window.location = 'mcba-ios:showToast'; }, " +
            "onMcbaReady: function() { setTimeout(function() { window.location = 'mcba-ios:onMcbaReady' }, 500); }, " +
            "exit: function() { } " +
        "};" +
        "console = new Object();" +
        "console.log = function(text) { window.location = 'mcba-ios:log/' + text; };" +
        "console.debug = console.log;" +
        "console.info = console.log;" +
        "console.warn = console.log;" +
        "console.error = console.log;"
        runJs( cmd )
    }
    
    func registerForPush( url: String, mcbaId: Int, id: String ) {
        runJs( "MCBA.registerPushId('\(url)', \(mcbaId), '\(UIDevice.current.model)', 2, '\(id)');" )
    }
    
    func promoblast( message: String ) {
        runJs( "MCBA.onPromoblast('\(message)');" )
    }
    
    func runJs( js: String ) {
        webView.evaluateJavaScript( js ) { (result, error) in
            if error != nil {
                print( error!.localizedDescription )
            }
        }
    }
    
    func setMcbaReadyCallback( callback: @escaping McbaReadyCallback ) {
        if mcbaReady {
            callback()
        } else {
            mmcbaReadyCallback = callback
        }
    }
    
    func onPageLoaded( page: String ) {
        print( "Page Loaded: \(page)" )
    }
    
    func onScriptLoaded() {}
    func exit() {}
    func webView( _ webView: WKWebView, didFailLoadWithError error: Error ) {}
    func webViewDidStartLoad(_ webView: WKWebView) {}
    func webViewDidFinishLoad(_ webView: WKWebView) {}
    
    func log( _ text: String ) {
        debugPrint( "MCBA log: " + text )
    }
    
    func onMcbaReady() {
        print( "Mcba ready")
        mcbaReady = true
        if mmcbaReadyCallback != nil {
            mmcbaReadyCallback!()
        }
        print( "calling MCBA.load()..." )
        runJs( "MCBA.load();" )
    }
    
    func setTemplateRoot( _ root: String ) {
        print( "Template root: \(root)" )
    }
}
```

In this new class, we have added the implementation of the WKScriptMessageHandler protocol. We have also added several functions to communicate with the web view. This class is responsible for handling JavaScript messages and callbacks.

Next, we will implement a new class to handle push notifications. Add a new file 'PushNotificationHandler.swift' with the following code:

```swift
class PushNotificationHandler {
    let mainInstance = McbaConfiguration.sharedInstance()
    
    func registerForPush( url: String, mcbaId: Int, id: String ) {
        if (!mainInstance.isRegistered()) {
            mainInstance.setDestination( destinationArg: "chat" )
        }
    }
}
```

In this class, we have moved the registerForPush function from JavascriptInterface to this new class. This class is responsible for handling push notifications.

We will also create a new file 'RequestHandler.swift' with