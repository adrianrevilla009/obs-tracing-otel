import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;

/** Tiny Orders service. No OpenTelemetry code: the agent instruments the JDK HTTP server. */
public class App {
    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/orders/", ex -> {
            String id = ex.getRequestURI().getPath().substring("/orders/".length());
            byte[] body = ("id=" + id + ";status=PAID").getBytes();
            try { Thread.sleep(25); } catch (InterruptedException ignored) { }
            ex.sendResponseHeaders(200, body.length);
            ex.getResponseBody().write(body);
            ex.close();
        });
        server.start();
    }
}
