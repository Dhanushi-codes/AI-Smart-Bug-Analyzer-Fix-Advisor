package com.vidzai.backend.service;

import com.vidzai.backend.model.BugReport;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@Service
public class BugService {

    public String processBug(BugReport bugReport) {

        return "Bug Received Successfully: " + bugReport.getTitle();

    }

    public String processBugFile(MultipartFile file) throws IOException {

        String fileContent = new String(file.getBytes());

        BugReport bugReport = new BugReport();

        bugReport.setTitle(file.getOriginalFilename());
        bugReport.setDescription(fileContent);

        return processBug(bugReport);
    }
}