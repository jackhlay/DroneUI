import javax.swing.*;
import java.awt.*;

public class View {
    private JFrame frame;
    private JPanel topText, takeoffFields, LLfields, midText, centerPanel;
    private JLabel takeoffLabel, addLabel, toLat, toLong, additLat, additLong;
    private JTextField takeoffLat, takeoffLong, Lat, Long;
    private JButton generatePlan, addPoint;

    public View() {
        frame = new JFrame("Spot-on drone plan generator");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(new Dimension(1280, 720));
        frame.setLayout(new BorderLayout());

        topText = new JPanel();
        takeoffFields = new JPanel();
        LLfields = new JPanel();
        midText = new JPanel();
        centerPanel = new JPanel();  // Initialize centerPanel here

        takeoffLabel = new JLabel("Enter Takeoff Coordinates");
        addLabel = new JLabel("Add additional points");
        toLat = new JLabel("Takeoff Latitude");
        toLong = new JLabel("Takeoff Longitude");
        additLat = new JLabel("Additional Latitude");
        additLong = new JLabel("Additional Longitude");

        takeoffLat = new JTextField("Takeoff Latitude", 20);
        takeoffLong = new JTextField("Takeoff Longitude", 20);

        Lat = new JTextField("LATTITUDE", 20);
        Long = new JTextField("LONGITUDE", 20);

        generatePlan = new JButton("Generate Plan");
        addPoint = new JButton("Add Waypoint");

        takeoffFields.add(toLat);
        takeoffFields.add(takeoffLat);
        takeoffFields.add(toLong);
        takeoffFields.add(takeoffLong);
        takeoffFields.add(generatePlan);

        LLfields.add(additLat);
        LLfields.add(Lat);
        LLfields.add(additLong);
        LLfields.add(Long);
        LLfields.add(addPoint);

        centerPanel.setLayout(new BoxLayout(centerPanel, BoxLayout.Y_AXIS));
        centerPanel.add(takeoffLabel);
        centerPanel.add(takeoffFields);
        centerPanel.add(midText);
        centerPanel.add(addLabel);
        centerPanel.add(LLfields);

        frame.add(topText, BorderLayout.NORTH);
        frame.add(centerPanel, BorderLayout.CENTER);
    }

    public void display() {
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            View view = new View();
            view.display();
        });
    }
}
