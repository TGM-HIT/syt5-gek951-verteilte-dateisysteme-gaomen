package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.InputStream;

@RestController
public class MinioController {

    @Autowired
    private MinioService minioService;

    // Upload a file
    @PostMapping("/upload")
    public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile file) {
        try {
            String fileName = file.getOriginalFilename();
            minioService.uploadFile(fileName, file);
            return ResponseEntity.ok("File uploaded successfully! UwU");
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body("File upload failed! >.<");
        }
    }

    // Download a file
    @GetMapping("/download/{fileName}")
    public ResponseEntity<InputStream> downloadFile(@PathVariable String fileName) {
        try {
            InputStream fileStream = minioService.getFile(fileName);
            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + fileName)
                    .contentType(MediaType.APPLICATION_OCTET_STREAM)
                    .body(fileStream);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(404).body(null);
        }
    }

    // Delete a file
    @DeleteMapping("/delete/{fileName}")
    public ResponseEntity<String> deleteFile(@PathVariable String fileName) {
        try {
            minioService.deleteFile(fileName);
            return ResponseEntity.ok("File deleted successfully! (✧ω✧)");
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body("File deletion failed! T_T");
        }
    }
}
