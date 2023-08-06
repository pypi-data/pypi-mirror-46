# slowbreak

Library to connect to FIX servers, and make our own. We use slowbreak to connect to ROFEX and BYMA markets in Argentina. 
It was originally designed to work with FIX5.0sp2 but now is adapted to be also used with FIX 4.2+ 
It works with python 2.7 and python 3.5+ (tested with python 2.7 and 3.6)  

See the slowbreak/example folder for examples on how to use it. You can also check the slowbreak/test folder to see details on how to use the API.

You can also see the slowbreak tutorials in this playlist: https://www.youtube.com/watch?v=LKkyr2j9dOA&list=PLTQoyI2lMoFOpQ0j1EmIwv6A_GVcP4CdK

Developed by Aureliano Calvo for Eco Valores S.A.  

Distributed under MIT license (see LICENSE file for details) 

## Why is this named as slowbreak?

Less is named after more. We chosen this name as a reference to QuickFix, 
as we intend to fix several shortcomings we found when trying to use it in python.

## Guiding principles

### Pure python

We will try to keep as pure-python as possible with this library. 
In the case we find we need to have a non-pure python implementation for performance reasons, 
we will provide both the python implementation and the native one.

### FIX messages are lists of (number, value) pairs

FIX messages are just a list of pairs (number, value). The value is just a string. 
In this library we do not attempt to:

1. Give names to tag numbers.
2. Know the actual type of a field.

Why? Because they vary between implementations. We try to find the waist of the protocol. We believe that all the implementations 
treat messages as a list of pairs. This allows us to have really generic code in a lot of parts and avoid the XML fiasco that happens when you need a small 
change of types or names in QuickFix.

### Certificate authorities are insecure

While we support connecting via SSL to servers, we intentionally not use the PKI infrastructure. Why? 
Because when you trust 100 CAs if anyone of those betrays you then you are screwed. And algorithmic trading handles tons of cash. So there is a lot of 
incentive to do unproper things. Instead we propose to use the hash of the server certificate as a way 
to identify it, using a mechanism similar to the one used in ssh. 

### All messages are equivalent

We do no distinction between administrative messages and application messages. Any application may handle any message. This allows us to have the session 
handling as just another FIX application.

### FIX applications are stacked like network protocols

This gives us the posibility to have different aspects of the algorithmic trading separated. 
We have the SessionApp, which is usually the base of the stack in production, that handles sequence numbers, logons, heartbeats, etc.
On top of that you may implement something that controls that the orders you put in the market are not too big, also as an FixApplication.
And on top of that you can implement the logic of your trading strategy.

### We do not tell you how to trade

As we develop the library, we will be adding more functionallity. For instance, we intend to provide:

1. Applications to limit the position of your algorithm
2. Applications to limit the rate of messages sent to the server

What we will not provide is production-ready strategies for algorithmic trading.

### Testing is important

That's why we provide from the start the ability to unit test your strategies, without connecting to any market, and the ability to make your own server 
to do end to end testing. 

