import XCTest

@testable import HelloWorld

final class HelloWorldTests: XCTestCase {
    func testHelloWorld() {
        XCTAssertEqual(hello(), "Hello, world!")
    }
}