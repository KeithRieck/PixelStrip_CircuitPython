package frc.robot;

import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj.XboxController;
import frc.robot.subsystems.*;

/**
 * This robot program tests that animations on a Raspberry Pi Pico can be
 * controlled by the RoboRIO through I2C communications.
 */
public class Robot extends TimedRobot {

  LightsSubsystem m_LightsSubsystem;
  XboxController xbox;

  private int myStrip = 0;
  private int myAnim = 0;

  @Override
  public void robotInit() {
    xbox = new XboxController(0);
    m_LightsSubsystem = new LightsSubsystem();
  }

  @Override
  public void robotPeriodic() {
    m_LightsSubsystem.periodic();
  }

  @Override
  public void teleopInit() {
    myStrip = 0;
    myAnim = 0;
  }

  @Override
  public void teleopPeriodic() {
    if (xbox.getLeftBumperPressed()) {
      myAnim = (myAnim + 1) % m_LightsSubsystem.MAX_ANIMATIONS;
      m_LightsSubsystem.setAnimation(myStrip, myAnim);
    } else if (xbox.getRightBumperPressed()) {
      m_LightsSubsystem.clearAllAnimations();
    } else if (xbox.getYButtonPressed()) {
      myStrip = 0;
    } else if (xbox.getBButtonPressed()) {
      myStrip = 1;
    } else if (xbox.getAButtonPressed()) {
      myStrip = 2;
    } else if (xbox.getXButtonPressed()) {
      myStrip = 3;
    }
  }

}
