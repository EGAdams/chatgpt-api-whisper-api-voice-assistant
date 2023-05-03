import UIKit
import WebKit
import Foundation
import CoreData

typealias McbaReadyCallback = () -> ()
class JavascriptInterface: NSObject, WKScriptMessageHandler {

func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
if message.name == "MCBA" {
guard let urlString = message.body as? String,
let url = URL(string: urlString) else {
return
}
let request = URLRequest(url: url)
parseRequest(request)
}
}

let scheme = "mcba-ios"
var mcbaReady = false
var webView: WKWebView!
var mmcbaReadyCallback: McbaReadyCallback?
var rewardsLoaded = false;

init( view: WKWebView! /* WKWebView! */ ){
print( "*** INITIALIZING JAVASCRIPT OBJECT HERE. ***" )
let global = McbaConfiguration.sharedInstance()
webView = view
super.init()
// webView.delegate = self // TODO: not sure about this either.

//webView.configuration.userContentController.add(self, name: "MCBA")
bind() // TODO: not sure about this???

if (!global.isJavascriptInitialized()) {
print( "*** SETTING var Device = { ... ***" )
// bind() TODO: above bind may be here, not sure
global.javascriptInitialized = true
}
print( "*** INITIALIZING JAVASCRIPT INIT FUNCTION. ***" )
}

func runJs(_ js: String!) {
webView.evaluateJavaScript(js) { (result, error) in
if error != nil { print(error!.localizedDescription) }}}

func bind(){
let cmd = "var Device = { " +
"setTemplateRoot : function(root){}," +
"onPageLoaded : function(page){ window.location = 'mcba-ios:onPageLoaded/'+page; }," +
"onScriptLoaded : function(src){ }," +
"showToast : function(msg){ window.location = 'mcba-ios:showToast'; }," +
// "onMcbaReady : function(){ window.location = 'mcba-ios:onMcbaReady';}," +
"onMcbaReady : setTimeout( function(){ window.location = 'mcba-ios:onMcbaReady';}, 500 );," +
"exit : function(){}" +
"};" +
"console = new Object();" +
"console.log = function(text){" +
"window.location = 'mcba-ios:log/'+text;" +
"};" +
"console.debug = console.log;" +
"console.info = console.log;" +
"console.warn = console.log;" +
"console.error = console.log;"

runJs( cmd )
}

func registerForPush( _ url: String!, mcbaId: Int!, id: String! ){
print( "Registering: \(String(describing: id))" )
runJs( "MCBA.registerPushId('\(String(describing: url))', \(String(describing: mcbaId)),'\(UIDevice.current.model)', 2,'\(id)');" )
print("We should be registered remotely now")
}

func promoblast( _ message: String! ){
runJs( "MCBA.onPromoblast('\(String(describing: message))');")
}

func parseRequest( _ request: URLRequest! ){
if ( request == nil ) {
print( "request is nil! returning... " )
return
}
if request.url!.scheme == self.scheme {
let urlString = request.url!.absoluteURL.absoluteString.replacingOccurrences(of: self.scheme + ":", with: "")
let params = urlString.components(separatedBy: "/")
let funcName = params[0]
print("funcName:\(funcName)")
switch funcName {
case "onPageLoaded":
onPageLoaded(params[1])
break
case "setTemplateRoot":
setTemplateRoot( params[1] )
break
case "onMcbaReady":
print( "calling onMcbaReady()... " )
onMcbaReady()
break
case "exit":
break
case "log":
log( params[1] )
break
default:
break
}
}
}

func log(_ text: String!){
debugPrint("MCBA log: " + text)
}

func onMcbaReady(){
print("Mcba ready")
self.mcbaReady = true
if mmcbaReadyCallback != nil{
mmcbaReadyCallback!()
}
print( "calling MCBA.load()... " )
runJs("MCBA.load();")
}

func setMcbaReadyCallback( _ callback: McbaReadyCallback! ){
if mcbaReady {
callback()
} else {
self.mmcbaReadyCallback = callback
}
}


func setTemplateRoot( _ root: String! ){
print("Template root: " + root)
}

func onPageLoaded(_ page: String){
print("Page Loaded: \(page)")
}

func onScriptLoaded(){}

func exit(){
print ( "exiting... " )
}

func webView(_ webView: WKWebView, didFailLoadWithError error: Error) {}

func webView(_ webView: WKWebView, shouldStartLoadWith request: URLRequest, navigationType: WKWebView.Type ) -> Bool {
parseRequest(request)

////////////////////////// copied from url protocol on Friday august 3, 2018 ///////////////////////////////////
let mainInstance = McbaConfiguration.sharedInstance()
let mLibraryBundle = Bundle(identifier: "awm.ios.mcba.mLibrary")
let mainStoryBoard = UIStoryboard(name: "mcbaStoryboard", bundle: mLibraryBundle)

if var topController = UIApplication.shared.keyWindow?.rootViewController {
while let presentedViewController = topController.presentedViewController {
topController = presentedViewController
}
let requestString = request.url?.absoluteString

if (requestString!.containsIgnoringCase(find: "chat")) {

let defaults = UserDefaults.standard
if (!mainInstance.isRegistered()) {
mainInstance.setDestination(destinationArg: "chat")
print("// JavascriptInterface: Switch to SignIn")
let vc : UIViewController = mainStoryBoard.instantiateViewController(withIdentifier: "SignInEntry")
topController.show(vc as UIViewController, sender: vc)
} else {
let libraryDelegate = mLibrary.LibraryDelegate.sharedInstance()
if(!libraryDelegate.initializeChat()) {
return false
}
} // end if is registered
}// end if is a chat message

if (requestString!.containsIgnoringCase(find: "rewards")) {

if (!mainInstance.isRegistered()) {
print("// JavascriptInterface: Switch to SignIn")
let vc : UIViewController = mainStoryBoard.instantiateViewController(withIdentifier: "SignInEntry")
topController.show(vc as UIViewController, sender: vc)
} else {
print("// JavascriptInterface: Switch to Rewards")
if ( self.rewardsLoaded == false ) {
self.rewardsLoaded = true
let vc : UIViewController = mainStoryBoard.instantiateViewController(withIdentifier: "RewardsEntry")
topController.show(vc as UIViewController, sender: vc)
}
}
}

if (requestString!.containsIgnoringCase(find: "navigate")) {
let mapObject = Map()
mapObject.openMapForPlace()
}

if (requestString!.containsIgnoringCase(find: "geofence")) {

let vc : UIViewController = mainStoryBoard.instantiateViewController(withIdentifier: "GeofenceEntry")
topController.show(vc as UIViewController, sender: vc)
}

if (requestString!.containsIgnoringCase(find: "shop")) {
let vc = mainStoryBoard.instantiateViewController(withIdentifier: "shopView") as! shopController
topController.show(vc, sender: vc)
}

if (request.url?.absoluteString == "mcba://webView") {
let vc = mainStoryBoard.instantiateViewController(withIdentifier: "view") as! ViewController
topController.show(vc, sender: vc)
}
}
return true
}

func resetDefaults() {
let defaults = UserDefaults.standard
let dictionary = defaults.dictionaryRepresentation()
dictionary.keys.forEach { key in
defaults.removeObject(forKey: key)
}
}

func webViewDidStartLoad(_ webView: WKWebView) {
print ( "web view did start load... " )
}
func webViewDidFinishLoad(_ webView: WKWebView) {
print ( "web view did finish load. " )
}

func printDefaults() {
let defaults = UserDefaults.standard
let dictionary = defaults.dictionaryRepresentation()
dictionary.keys.forEach { key in
print ("key: \(key)")
}
}
}

extension String {
func contains(find: String) -> Bool{
return self.range(of: find) != nil
}
func containsIgnoringCase(find: String) -> Bool{
return self.range(of: find, options: .caseInsensitive) != nil
}
}