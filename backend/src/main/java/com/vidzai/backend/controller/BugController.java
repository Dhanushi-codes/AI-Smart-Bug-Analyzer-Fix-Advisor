package com.vidzai.backend.controller;

import com.vidzai.backend.model.BugReport;
import org.springframework.web.bind.annotation.*;

@RestController
public class BugController {

    @PostMapping("/submitBug")
    public String submitBug(@RequestBody BugReport bugReport) {

        return "Bug Received: " + bugReport.getBugReport();

    }

}