import javax.swing.*;
import java.awt.*;

public class View {
    //Build the gui
    private JFrame frame;
    private JPanel topText, takeoffFields, LLfields, midText, centerPanel;
    private JLabel takeoffLabel, addLabel, toLat, toLong, additLat, additLong;
    private JTextField takeoffLat, takeoffLong, Lat, Long;
    private JButton generatePlan, addPoint;

    public View() {
        //Window frame block
        frame = new JFrame("Spot-on drone plan generator");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(new Dimension(800, 600));
        frame.setResizable(false);
        frame.setLayout(new BorderLayout());

        //Creating necessary panels
        topText = new JPanel();
        takeoffFields = new JPanel();
        LLfields = new JPanel();
        midText = new JPanel();
        centerPanel = new JPanel();  // Initialize centerPanel here

        //Creating necessary labels
        takeoffLabel = new JLabel("Enter Takeoff Coordinates");
        addLabel = new JLabel("Add additional points");
        toLat = new JLabel("Takeoff Latitude");
        toLong = new JLabel("Takeoff Longitude");
        additLat = new JLabel("Additional Latitude");
        additLong = new JLabel("Additional Longitude");

        //Creating necessary text fields
        takeoffLat = new JTextField("Takeoff Latitude", 20);
        takeoffLong = new JTextField("Takeoff Longitude", 20);
        Lat = new JTextField("LATTITUDE", 20);
        Long = new JTextField("LONGITUDE", 20);

        //Creating necessary buttons
        generatePlan = new JButton("Generate Plan");
        addPoint = new JButton("Add Waypoint");

        //adding takeOff fields to take off panel
        takeoffFields.add(toLat);
        takeoffFields.add(takeoffLat);
        takeoffFields.add(toLong);
        takeoffFields.add(takeoffLong);

        //adding fields for additional points to additional Points Panel
        LLfields.add(additLat);
        LLfields.add(Lat);
        LLfields.add(additLong);
        LLfields.add(Long);
        LLfields.add(addPoint);

        //adding Takeoff & additionalPoints panels to a central panel.
        centerPanel.setLayout(new BoxLayout(centerPanel, BoxLayout.Y_AXIS));
        centerPanel.add(takeoffLabel);
        centerPanel.add(takeoffFields);
        centerPanel.add(midText);
        centerPanel.add(addLabel);
        centerPanel.add(LLfields);
        centerPanel.add(generatePlan);

        //adding final panel to window
        frame.add(topText, BorderLayout.NORTH);
        frame.add(centerPanel, BorderLayout.CENTER);
    }

    //displays window when called.
    public void display() {
        frame.setVisible(true);
    }
}
