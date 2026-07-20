package com.vidzai.backend.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BugController {

    @GetMapping("/")
    public String home() {
        return "AI Smart Bug Analyzer Backend is Running!";
    }

}