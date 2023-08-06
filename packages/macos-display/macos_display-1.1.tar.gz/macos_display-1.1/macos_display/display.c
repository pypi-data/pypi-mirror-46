//
// Created by Robert Smallshire on 2019-05-23.
//

#include "display.h"

#include <IOKit/graphics/IOGraphicsLib.h>
#include <CoreVideo/CVBase.h>
#include <CoreVideo/CVDisplayLink.h>
#include <ApplicationServices/ApplicationServices.h>



// Returns the io_service_t corresponding to a CG display ID, or 0 on failure.
// The io_service_t should be released with IOObjectRelease when not needed.
// The implementation in this function is based on an open-source version
// which is part of the GLFW library, with various fixes, found in
// https://github.com/glfw/glfw/blob/master/src/cocoa_monitor.m by
// Copyright (c) 2002-2006 Marcus Geelnard Copyright (c) 2006-2016 Camilla Löwy elmindreda@glfw.org
io_service_t IOServicePortFromCGDisplayID(CGDirectDisplayID displayID)
{
    const int MAX_DISPLAYS = 16;
    CGDisplayCount    displayCount;
    CGDisplayCount    maxDisplays = MAX_DISPLAYS;
    CGDirectDisplayID onlineDisplays[MAX_DISPLAYS];
    CGDisplayErr dErr = CGGetOnlineDisplayList(maxDisplays, onlineDisplays, &displayCount);
    if (dErr != kCGErrorSuccess) {
        return 0;
    }

    io_iterator_t iter;
    io_service_t serv, servicePort = 0;

    CFMutableDictionaryRef matching = IOServiceMatching("IODisplayConnect");

    // releases matching for us
    kern_return_t err = IOServiceGetMatchingServices(kIOMasterPortDefault,
                                                     matching,
                                                     &iter);
    if (err)
    {
        return 0;
    }

    while ((serv = IOIteratorNext(iter)) != 0)
    {
        CFDictionaryRef info;
        CFIndex vendorID, productID, serialID;
        CFNumberRef vendorIDRef, productIDRef, serialIDRef;
        Boolean success;

        info = IODisplayCreateInfoDictionary(serv,
                                             kIODisplayOnlyPreferredName);

        vendorIDRef = CFDictionaryGetValue(info,
                                           CFSTR(kDisplayVendorID));
        productIDRef = CFDictionaryGetValue(info,
                                            CFSTR(kDisplayProductID));
        serialIDRef = CFDictionaryGetValue(info,
                                           CFSTR(kDisplaySerialNumber));

        success = CFNumberGetValue(vendorIDRef, kCFNumberCFIndexType,
                                   &vendorID);
        success &= CFNumberGetValue(productIDRef, kCFNumberCFIndexType,
                                    &productID);
        if (serialIDRef != 0) {
            success &= CFNumberGetValue(serialIDRef, kCFNumberCFIndexType,
                                    &serialID);
        }

        if (!success)
        {
            CFRelease(info);
            continue;
        }

        if (CGDisplayVendorNumber(displayID) != vendorID ||
            CGDisplayModelNumber(displayID) != productID)
        {
            CFRelease(info);
            continue;
        }

        // we're a match
        servicePort = serv;
        CFRelease(info);
        break;
    }

    IOObjectRelease(iter);
    return servicePort;
}

// Get the name of the specified display
//
char* getDisplayName(CGDirectDisplayID displayID)
{
    io_service_t serv = IOServicePortFromCGDisplayID(displayID);
    if (!serv)
    {
        return strdup("Unknown");
    }

    CFDictionaryRef info = IODisplayCreateInfoDictionary(serv,
                                         kIODisplayOnlyPreferredName);

    IOObjectRelease(serv);

    CFStringRef value;

    CFDictionaryRef names = CFDictionaryGetValue(info, CFSTR(kDisplayProductName));

    if (!names || !CFDictionaryGetValueIfPresent(names, CFSTR("en_US"),
                                                 (const void**) &value))
    {
        CFRelease(info);
        return strdup("Unknown");
    }

    CFIndex size = CFStringGetMaximumSizeForEncoding(CFStringGetLength(value),
                                             kCFStringEncodingUTF8);
    char* name = calloc((size_t) (size + 1), 1);
    CFStringGetCString(value, name, size, kCFStringEncodingUTF8);

    CFRelease(info);

    return name;
}
