package com.astro.languagereactor

import android.annotation.SuppressLint
import android.os.Bundle
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.CircularProgressIndicator
import androidx.compose.material.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import kotlinx.coroutines.delay

class MainActivity : ComponentActivity() {
    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            var showSplash by remember { mutableStateOf(true) }
            var webView: WebView? by remember { mutableStateOf(null) }
            var canGoBack by remember { mutableStateOf(false) }

            // Splash Screen Timer
            LaunchedEffect(Unit) {
                delay(2500) // Tampilkan splash selama 2.5 detik
                showSplash = false
            }

            // Handle hardware back button
            BackHandler(enabled = canGoBack) {
                webView?.goBack()
            }

            Box(modifier = Modifier.fillMaxSize().background(Color(0xFF121212))) {
                // The main WebView
                AndroidView(
                    modifier = Modifier.fillMaxSize(),
                    factory = { context ->
                        WebView(context).apply {
                            settings.apply {
                                javaScriptEnabled = true
                                domStorageEnabled = true
                                databaseEnabled = true
                                useWideViewPort = true
                                loadWithOverviewMode = true
                                builtInZoomControls = false
                                displayZoomControls = false
                                setSupportZoom(true)
                                
                                // Standard mobile view
                                userAgentString = null
                            }
                            
                            webViewClient = object : WebViewClient() {
                                override fun onPageFinished(view: WebView?, url: String?) {
                                    super.onPageFinished(view, url)
                                    canGoBack = view?.canGoBack() ?: false
                                }

                                override fun shouldOverrideUrlLoading(
                                    view: WebView?,
                                    request: WebResourceRequest?
                                ): Boolean {
                                    return false
                                }
                            }
                            
                            loadUrl("https://www.languagereactor.com")
                            webView = this
                        }
                    },
                    update = {
                        webView = it
                    }
                )

                // Splash Screen Overlay (Overlaying WebView so it loads in background)
                AnimatedVisibility(
                    visible = showSplash,
                    exit = fadeOut(),
                    modifier = Modifier.fillMaxSize()
                ) {
                    SplashUI()
                }
            }
        }
    }
}

@Composable
fun SplashUI() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF121212)),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Mock Logo (Placeholder for Language Reactor icon)
        Text(
            text = "LANGUAGE",
            color = Color(0xFF4CAF50),
            fontSize = 40.sp,
            fontWeight = FontWeight.Bold
        )
        Text(
            text = "REACTOR",
            color = Color(0xFFE0E0E0),
            fontSize = 32.sp,
            letterSpacing = 8.sp,
            fontWeight = FontWeight.Light
        )
        
        Spacer(modifier = Modifier.height(60.dp))
        
        CircularProgressIndicator(
            color = Color(0xFF4CAF50),
            strokeWidth = 3.dp
        )
    }
}
