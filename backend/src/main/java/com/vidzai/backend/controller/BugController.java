package com.vidzai.backend.controller;

import com.vidzai.backend.model.BugReport;
import com.vidzai.backend.service.BugService;
import org.springframework.web.bind.annotation.*;

@RestController
public class BugController {

    private final BugService bugService;

    public BugController(BugService bugService) {
        this.bugService = bugService;
    }

    @PostMapping("/submitBug")
    public String submitBug(@RequestBody BugReport bugReport) {

        return bugService.processBug(bugReport);

    }
}