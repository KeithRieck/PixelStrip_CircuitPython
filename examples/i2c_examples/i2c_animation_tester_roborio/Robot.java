package frc.robot;

import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj.I2C;
import edu.wpi.first.wpilibj.I2C.Port;

/**
 * This robot program tests that animations on a Raspberry Pi Pico can be
 * controlled by the RoboRIO through I2C communications.
 */
public class Robot extends TimedRobot {

  public static int I2C_ADDRESS = 0x41;
  public static final int MAX_ANIMATIONS = 3;
  public static final int MAX_STRIPS = 4;

  private byte[] currentAnimation = new byte[MAX_STRIPS];
  private byte[] nextAnimation = new byte[MAX_STRIPS];
  private int myStrip = 0;
  private int myAnim = 0;
  private byte[] dataOut = new byte[1];

  private XboxController xbox = null;
  private I2C i2c = null;

  @Override
  public void robotInit() {
    xbox = new XboxController(0);
    i2c = new I2C(Port.kOnboard, I2C_ADDRESS);
    clearAllAnimations();
  }

  /**
   * Pressing the Left bumper button will change the animation on one of the strips.
   * Pressing any of the A, B, X, or Y buttons selects which strip will be changed.
   * Pressing the Right bumper button clears out all strip animations.
   */
  @Override
  public void teleopPeriodic() {
    if (xbox.getLeftBumperPressed()) {
      myAnim = (myAnim + 1) % MAX_ANIMATIONS;
      setAnimation(myStrip, myAnim);
    } else if (xbox.getRightBumperPressed()) {
      clearAllAnimations();
    } else if (xbox.getYButtonPressed()) {
      myStrip = 0;
    } else if (xbox.getBButtonPressed()) {
      myStrip = 1;
    } else if (xbox.getAButtonPressed()) {
      myStrip = 2;
    } else if (xbox.getXButtonPressed()) {
      myStrip = 3;
    }
    sendAllAnimations();
  }

  /**
   * Clear out all the strips and stop all animation.
   */
  private void clearAllAnimations() {
    for (int s = 0; s < MAX_STRIPS; s++) {
      Integer b = Integer.valueOf(((s << 4) & 0xF0) | (MAX_ANIMATIONS & 0x0F));
      nextAnimation[s] = b.byteValue();
      currentAnimation[s] = (byte) 0;
    }
    myStrip = 0;
    myAnim = 0;
  }

  /**
   * Set one strip to have the numbered animation.
   */
  private void setAnimation(int stripNumber, int animNumber) {
    Integer b = Integer.valueOf(((stripNumber << 4) & 0xF0) | (animNumber & 0x0F));
    nextAnimation[stripNumber] = b.byteValue();
  }

  /**
   * Push out all animation changes to the Pico. <br/>
   * This program takes a <em>lazy</em> approach, in that animation signals are
   * only sent out if they <em>need</em> to change. Signals are only sent if the
   * desired animation is different from the current animation.
   * This prevents redundant, unnecessary changes from dominating the I2C bus.
   */
  private void sendAllAnimations() {
    for (int s = 0; s < MAX_STRIPS; s++) {
      if (nextAnimation[s] != currentAnimation[s]) {
        sendOneAnimation(s);
        currentAnimation[s] = nextAnimation[s];
      }
    }
  }

  private void sendOneAnimation(int stripNumber) {
    dataOut[0] = nextAnimation[stripNumber];
    i2c.writeBulk(dataOut, dataOut.length);
  }
}