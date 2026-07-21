package com.vidzai.backend.controller;

import com.vidzai.backend.model.BugReport;
import com.vidzai.backend.service.BugService;

import java.io.IOException;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

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

    @PostMapping("/submitBug/file")
public String submitBugFile(@RequestParam("file") MultipartFile file) throws IOException {

    return bugService.processBugFile(file);

}

    
}