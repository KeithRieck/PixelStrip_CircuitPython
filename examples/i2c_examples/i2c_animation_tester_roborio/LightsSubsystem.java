package frc.robot;

import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.I2C;
import edu.wpi.first.wpilibj.I2C.Port;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

/**
 * Subsystem to controll all the lights running on the external lights
 * microcontroller.
 * <p>
 * The whole "lights plan" should be implemented from within this subsystem,
 * controlled mostly from within the {@code periodic()} method.
 * <p>
 * If you need external subsystems and commands to communicate into this class,
 * create "modes" within the class to indicate external states. For instance,
 * if you need a command to indicate when the robot is preparing to shoot, add
 * a {@code setShootingMode(boolean)} to this class. Then, add code to the
 * {@code periodic()} that changes animations based on current modes.
 */
public class LightsSubsystem extends SubsystemBase {

  public static final int MAX_ANIMATIONS = 20; // Must be 32 or less
  public static final int MAX_STRIPS = 5; // Must be 8 or less
  public static int I2C_ADDRESS = 0x41;
  private static int MAX_PARAM = 64;

  private record AnimationState(int stripNumber, int animNumber, String param) {
  }

  private AnimationState[] currentAnimation = new byte[MAX_STRIPS];
  private AnimationState[] nextAnimation = new byte[MAX_STRIPS];
  private byte[] dataOut = new byte[MAX_PARAM];

  private I2C i2c = null;

  public LightsSubsystem() {
    i2c = new I2C(Port.kOnboard, I2C_ADDRESS);
    for (int s = 0; s < MAX_STRIPS; s++) {
      currentAnimation[s] = new AnimationState(s, 0, null);
      nextAnimation[s] = new AnimationState(s, MAX_ANIMATIONS, null);
    }
    clearAllAnimations();
  }

  @Override
  public void periodic() {
    // TODO: monitor internal robot state and change animations as necessary

    sendAllAnimations();
  }

  /**
   * Clear out all the strips and stop all animation.
   * <br>
   * This should not be called from outside this subsystem.
   */
  protected void clearAllAnimations() {
    for (int s = 0; s < MAX_STRIPS; s++) {
      nextAnimation[s].animNumber = MAX_ANIMATIONS;
      nextAnimation[s].param = null;
    }
  }

  /**
   * Set one strip to have the numbered animation.
   * <br>
   * This should not be called from outside this subsystem. It should only be
   * called from within the "Lights Plan" implemented within the {@code periodic}
   * method.
   */
  protected void setAnimation(int stripNumber, int animNumber, String param) {
    nextAnimation[stripNumber].animNumber = animNumber;
    nextAnimation[stripNumber].param = param;
  }

  /**
   * Push out all animation changes to the Lights Board. <br/>
   * This program takes a <em>lazy</em> approach, in that animation signals are
   * only sent out if they <em>need</em> to change. Signals are only sent if the
   * desired animation is different from the current animation.
   * This prevents redundant, unnecessary changes from dominating the I2C bus.
   */
  private void sendAllAnimations() {
    for (int s = 0; s < MAX_STRIPS; s++) {
      if (!nextAnimation[s].equals(currentAnimation[s]) {
        sendOneAnimation(s);
        currentAnimation[s].animNumber = nextAnimation[s].animNumber;
        currentAnimation[s].param = nextAnimation[s].param;
      }
    }
  }

  /**
   * Send out one message on I2C to change the animation on one strip to be one
   * specific animation. The {@code stripNumber} and {@code animNumber} are packed
   * into a single byte. If there is a {@code param} associated with this change,
   * it is concatentated onto the message.
   */
  private void sendOneAnimation(int stripNumber) {
    int dataLength = 0;
    int animNumber = nextAnimation[stripNumber].animNumber;
    Integer b = Integer.valueOf(((stripNumber << 5) & 0xE0) | (animNumber & 0x1F));
    dataOut[dataLength++] = b.byteValue();

    if (nextAnimation[stripNumber].param != null && nextAnimation[stripNumber].param.length() > 0) {
      for (int i = 0; i < nextAnimation[stripNumber].param.length() && i < MAX_PARAM; i++) {
        dataOut[dataLength++] = nextAnimation[stripNumber].param.getBytes()[i];
      }
    }

    i2c.writeBulk(dataOut, dataLength);
  }
}
